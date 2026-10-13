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
        Hook running before LLM invocation:
        1. Stores human messages in long-term memory store
        2. Retrieves relevant user profile/preferences
        3. Appends retrieved context to the conversation
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
        
        last_human_msg = None
        for msg in reversed(messages):
            if isinstance(msg, HumanMessage):
                last_human_msg = msg
                break
                
        if last_human_msg is not None:
            # 1. Store human message
            try:
                store.put(namespace, str(uuid.uuid4()), {"message": last_human_msg})
            except Exception as e:
                print(f"Error saving message to AgentCore memory store: {e}")
                
            # 2. Retrieve relevant memories across sessions
            user_preferences_namespace = (actor_id,)
            try:
                preferences = store.search(
                    user_preferences_namespace, 
                    query=last_human_msg.content, 
                    limit=5
                )
                
                # 3. Inject retrieved memory into system context
                if preferences:
                    memories = []
                    for item in preferences:
                        val = item.value.get("message", "")
                        if val:
                            memories.append(val)
                            
                    if memories:
                        memory_context = "\n".join([f"- {m}" for m in memories])
                        memory_message = SystemMessage(
                            content=(
                                "The following are relevant profile details and memories recalled from your previous "
                                f"conversations with this user (Actor ID: {actor_id}):\n{memory_context}\n"
                                "Use this context to personalize your responses and recall user parameters automatically."
                            )
                        )
                        new_messages = []
                        if messages and getattr(messages[0], "type", "") == "system":
                            new_messages = [messages[0], memory_message] + messages[1:]
                        else:
                            new_messages = [memory_message] + messages
                            
                        return {"messages": new_messages}
            except Exception as e:
                print(f"AgentCore memory search error: {e}")
                
        return None

    @override
    def after_model(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
        """Hook running after LLM invocation to persist assistant outputs."""
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
        
        last_ai_msg = None
        for msg in reversed(messages):
            if isinstance(msg, AIMessage):
                last_ai_msg = msg
                break
                
        if last_ai_msg is not None and last_ai_msg.content:
            try:
                store.put(namespace, str(uuid.uuid4()), {"message": last_ai_msg})
            except Exception as e:
                print(f"Error saving assistant message to AgentCore memory store: {e}")
                
        return None
