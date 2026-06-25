import uuid
from typing import Any
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain.agents.middleware import AgentMiddleware, AgentState
from langgraph.config import get_config
from langgraph.runtime import Runtime
from typing_extensions import override

class MemoryMiddleware(AgentMiddleware):
    @override
    def before_model(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
        """
        Hook that runs before LLM invocation to:
        1. Save the latest human message to long-term memory
        2. Retrieve relevant user preferences and memories
        3. Append memories to the context as a system message
        """
        config = get_config()
        configurable = config.get("configurable", {})
        actor_id = configurable.get("actor_id")
        thread_id = configurable.get("thread_id")
        
        if not actor_id or not thread_id:
            return None
            
        store = runtime.store
        if not store:
            return None
            
        # Namespace for this specific session
        namespace = (actor_id, thread_id)
        messages = state.get("messages", [])
        
        # Find the last human message to save and search
        last_human_msg = None
        for msg in reversed(messages):
            if isinstance(msg, HumanMessage):
                last_human_msg = msg
                break
                
        if last_human_msg is not None:
            # 1. Save the latest human message to long-term memory
            try:
                store.put(namespace, str(uuid.uuid4()), {"message": last_human_msg.content})
            except Exception as e:
                print(f"Error saving user message to store: {e}")
                
            # 2. Retrieve relevant user preferences and memories (across all sessions/threads for this actor)
            # Use namespace (actor_id,) to look up preferences/history
            user_preferences_namespace = (actor_id,)
            try:
                preferences = store.search(
                    user_preferences_namespace, 
                    query=last_human_msg.content, 
                    limit=5
                )
                
                # 3. If we found relevant memories, add them to the context as a SystemMessage
                if preferences:
                    memories = []
                    for item in preferences:
                        val = item.value.get("message", "")
                        if val:
                            memories.append(val)
                            
                    if memories:
                        memory_context = "\n".join([f"- {m}" for m in memories])
                        print(f"Retrieved memories: {memory_context}")
                        
                        # Inject retrieved memories into the context
                        memory_message = SystemMessage(
                            content=(
                                "The following are relevant memories and preferences retrieved from your previous "
                                f"conversations with this user (Actor ID: {actor_id}):\n{memory_context}\n"
                                "Use this context to personalize your responses when relevant."
                            )
                        )
                        # We return the new list of messages with the system memory message prepended
                        # (usually after the first system prompt message if there is one)
                        new_messages = []
                        if messages and getattr(messages[0], "type", "") == "system":
                            new_messages = [messages[0], memory_message] + messages[1:]
                        else:
                            new_messages = [memory_message] + messages
                            
                        return {"messages": new_messages}
            except Exception as e:
                print(f"Memory retrieval error: {e}")
                
        return None

    @override
    def after_model(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
        """
        Hook that runs after LLM invocation to save AI messages to long-term memory
        """
        config = get_config()
        configurable = config.get("configurable", {})
        actor_id = configurable.get("actor_id")
        thread_id = configurable.get("thread_id")
        
        if not actor_id or not thread_id:
            return None
            
        store = runtime.store
        if not store:
            return None
            
        namespace = (actor_id, thread_id)
        messages = state.get("messages", [])
        
        # Save the last AI message to the long-term memory store
        for msg in reversed(messages):
            if isinstance(msg, AIMessage):
                try:
                    store.put(namespace, str(uuid.uuid4()), {"message": msg.content})
                except Exception as e:
                    print(f"Error saving assistant message to store: {e}")
                break
                
        return None
