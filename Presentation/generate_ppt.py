import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # Blank slide layout

    # Theme Colors
    BG_COLOR = RGBColor(7, 11, 19)
    TEXT_WHITE = RGBColor(248, 250, 252)
    TEXT_MUTED = RGBColor(148, 163, 184)
    ACCENT_CYAN = RGBColor(0, 242, 254)
    ACCENT_PURPLE = RGBColor(138, 43, 226)
    ACCENT_GOLD = RGBColor(241, 196, 15)
    CARD_BG = RGBColor(15, 23, 42)
    BORDER_COLOR = RGBColor(31, 45, 71)

    def set_slide_background(slide):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = BG_COLOR

    def add_header(slide, section_label, title_text):
        # Section Label
        lbl_box = slide.shapes.add_textbox(Inches(0.75), Inches(0.4), Inches(11.833), Inches(0.3))
        tf_lbl = lbl_box.text_frame
        tf_lbl.word_wrap = True
        tf_lbl.margin_left = tf_lbl.margin_right = tf_lbl.margin_top = tf_lbl.margin_bottom = 0
        p_lbl = tf_lbl.paragraphs[0]
        p_lbl.text = section_label.upper()
        p_lbl.font.name = 'Arial'
        p_lbl.font.size = Pt(10)
        p_lbl.font.bold = True
        p_lbl.font.color.rgb = ACCENT_CYAN
        
        # Title
        title_box = slide.shapes.add_textbox(Inches(0.75), Inches(0.7), Inches(11.833), Inches(0.7))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        tf_title.margin_left = tf_title.margin_right = tf_title.margin_top = tf_title.margin_bottom = 0
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.name = 'Arial'
        p_title.font.size = Pt(26)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_WHITE

    def add_speaker_notes(slide, notes_text):
        notes_slide = slide.notes_slide
        text_frame = notes_slide.notes_text_frame
        text_frame.text = notes_text

    def create_card_shape(slide, left, top, width, height, bg_rgb, border_rgb):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_rgb
        shape.line.color.rgb = border_rgb
        shape.line.width = Pt(1.5)
        # remove text wrapping margin
        tf = shape.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = Inches(0.15)
        return shape

    # =========================================================================
    # SLIDE 1: Title Slide
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1)
    
    # Title Text Box
    title_box = slide1.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(11.333), Inches(3.5))
    tf1 = title_box.text_frame
    tf1.word_wrap = True
    
    p1 = tf1.paragraphs[0]
    p1.text = "AWS BEDROCK &"
    p1.font.name = 'Arial'
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE
    p1.alignment = PP_ALIGN.CENTER
    
    p2 = tf1.add_paragraph()
    p2.text = "AMAZON BEDROCK AGENTCORE"
    p2.font.name = 'Arial'
    p2.font.size = Pt(44)
    p2.font.bold = True
    p2.font.color.rgb = ACCENT_PURPLE
    p2.alignment = PP_ALIGN.CENTER
    p2.space_before = Pt(10)
    
    p3 = tf1.add_paragraph()
    p3.text = "A comprehensive educator guide to building, deploying, and scaling secure enterprise-grade AI agents."
    p3.font.name = 'Arial'
    p3.font.size = Pt(18)
    p3.font.color.rgb = TEXT_MUTED
    p3.alignment = PP_ALIGN.CENTER
    p3.space_before = Pt(30)

    p4 = tf1.add_paragraph()
    p4.text = "SCHOOL OF CLOUD AI ARCHITECTURES  •  LECTURE SLIDES"
    p4.font.name = 'Arial'
    p4.font.size = Pt(11)
    p4.font.bold = True
    p4.font.color.rgb = ACCENT_CYAN
    p4.alignment = PP_ALIGN.CENTER
    p4.space_before = Pt(50)

    add_speaker_notes(slide1, 
        "Welcome Students. Today we are discussing generative AI architectures on AWS. "
        "Specifically, we will start with AWS Bedrock (the models and foundation level) "
        "and then explore Bedrock AgentCore—the new managed framework for orchestrating, running, and scaling secure AI agents.")

    # =========================================================================
    # SLIDE 2: Demystifying AWS Bedrock
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2)
    add_header(slide2, "AWS Bedrock Overview", "Demystifying AWS Bedrock")

    # Left Column (Overview & Mission)
    left_box = slide2.shapes.add_textbox(Inches(0.75), Inches(1.8), Inches(5.5), Inches(4.5))
    tf2_left = left_box.text_frame
    tf2_left.word_wrap = True
    
    p_desc = tf2_left.paragraphs[0]
    p_desc.text = "Amazon Bedrock is a fully managed, serverless AWS service that provides developer access to high-performing foundation models (FMs) via a single, unified API."
    p_desc.font.name = 'Arial'
    p_desc.font.size = Pt(18)
    p_desc.font.color.rgb = TEXT_WHITE
    p_desc.space_after = Pt(20)

    p_mission_lbl = tf2_left.add_paragraph()
    p_mission_lbl.text = "Core Value Proposition:"
    p_mission_lbl.font.name = 'Arial'
    p_mission_lbl.font.size = Pt(14)
    p_mission_lbl.font.bold = True
    p_mission_lbl.font.color.rgb = ACCENT_CYAN
    p_mission_lbl.space_after = Pt(6)

    p_mission = tf2_left.add_paragraph()
    p_mission.text = "Bedrock abstracts away the complexities of hosting and running massive machine learning models, allowing developers to focus on application logic, prompting strategies, and enterprise security configurations."
    p_mission.font.name = 'Arial'
    p_mission.font.size = Pt(14)
    p_mission.font.color.rgb = TEXT_MUTED

    # Right Column (Cards)
    right_positions = [
        ("Unified API Access", "One unified client API connects you to multiple leading model providers: Anthropic (Claude), Meta (Llama), Mistral AI, Cohere, and Amazon Titan.", Inches(1.8), ACCENT_CYAN),
        ("Enterprise Security", "Your data is encrypted, stays within your VPC, and is never shared with third-party model providers or used to train their base weights.", Inches(3.3), ACCENT_PURPLE),
        ("Serverless Scale", "Zero servers to provision. Pays only for consumed tokens (input/output) or provisioned throughput for predictable execution.", Inches(4.8), ACCENT_GOLD)
    ]
    for title, desc, top, accent in right_positions:
        card = create_card_shape(slide2, Inches(6.75), top, Inches(5.833), Inches(1.2), CARD_BG, BORDER_COLOR)
        tf_card = card.text_frame
        
        p_c1 = tf_card.paragraphs[0]
        p_c1.text = title
        p_c1.font.name = 'Arial'
        p_c1.font.size = Pt(14)
        p_c1.font.bold = True
        p_c1.font.color.rgb = accent
        p_c1.space_after = Pt(4)
        
        p_c2 = tf_card.add_paragraph()
        p_c2.text = desc
        p_c2.font.name = 'Arial'
        p_c2.font.size = Pt(11)
        p_c2.font.color.rgb = TEXT_MUTED

    add_speaker_notes(slide2, 
        "AWS Bedrock is the foundation layer. Key point: it is serverless. "
        "Explain to students that instead of configuring EC2 instances with GPUs to run Llama or Claude, "
        "they get an AWS SDK client that invokes them with simple API keys. Data security is a key selling point.")

    # =========================================================================
    # SLIDE 3: Key Services Under Bedrock
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3)
    add_header(slide3, "AWS Bedrock Capabilities", "Key Services Under Bedrock")

    # 4 horizontal cards
    card_width = Inches(2.7)
    card_height = Inches(4.4)
    gap = Inches(0.3)
    start_left = Inches(0.75)
    
    services = [
        ("01", "Knowledge Bases", "Out-of-the-box Retrieval-Augmented Generation (RAG). Automatically syncs documents in S3, handles chunking and embedding, and loads them into vector databases (OpenSearch, Pinecone) for context-aware querying."),
        ("02", "Guardrails", "Apply custom safety filters. Blocks prohibited topics using simple keyword or natural language rules, filters toxic content, and masks PII (Personally Identifiable Information) before model input or after output."),
        ("03", "Model Customization", "Fine-tune model weights or run continued pre-training on proprietary datasets securely. You can also import custom weights directly via Custom Model Import and host them inside Bedrock."),
        ("04", "Model Evaluation", "Compare foundation models side-by-side using automatic criteria (accuracy, toxicity) or human evaluation tasks to select the most cost-effective and capable foundation model for your workload.")
    ]

    for i, (num, title, desc) in enumerate(services):
        left = start_left + i * (card_width + gap)
        card = create_card_shape(slide3, left, Inches(1.8), card_width, card_height, CARD_BG, BORDER_COLOR)
        tf_card = card.text_frame
        
        p_num = tf_card.paragraphs[0]
        p_num.text = num
        p_num.font.name = 'Arial'
        p_num.font.size = Pt(20)
        p_num.font.bold = True
        p_num.font.color.rgb = ACCENT_CYAN
        p_num.space_after = Pt(8)
        
        p_title = tf_card.add_paragraph()
        p_title.text = title
        p_title.font.name = 'Arial'
        p_title.font.size = Pt(16)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_WHITE
        p_title.space_after = Pt(12)
        
        p_desc = tf_card.add_paragraph()
        p_desc.text = desc
        p_desc.font.name = 'Arial'
        p_desc.font.size = Pt(11)
        p_desc.font.color.rgb = TEXT_MUTED

    add_speaker_notes(slide3, 
        "Make sure to explain the difference between a raw model and these services. "
        "Knowledge Bases automates the RAG pipeline. "
        "Guardrails is the firewall. "
        "Model Customization allows tweaking models for specific domains (like medical or legal terms). "
        "Model Evaluation helps with the business decision of choosing models.")

    # =========================================================================
    # SLIDE 4: Transitioning to Agents
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4)
    add_header(slide4, "The Shift to Agents", "From Simple Prompts to Autonomous Agents")

    # Left Column
    left_box = slide4.shapes.add_textbox(Inches(0.75), Inches(1.8), Inches(5.5), Inches(4.5))
    tf4_left = left_box.text_frame
    tf4_left.word_wrap = True
    
    p_desc = tf4_left.paragraphs[0]
    p_desc.text = "Standard LLMs are passive: they wait for a prompt, process it, and output text. In contrast, AI Agents are active loops that can plan, reason, invoke external tools, and remember context across sessions."
    p_desc.font.name = 'Arial'
    p_desc.font.size = Pt(16)
    p_desc.font.color.rgb = TEXT_WHITE
    p_desc.space_after = Pt(30)

    p_quote = tf4_left.add_paragraph()
    p_quote.text = '"The hardest part of building AI agents isn\'t writing the first prototype loop; it\'s secure deployment, scaling session memory, managing identity permissions, and evaluating behavior in production."'
    p_quote.font.name = 'Arial'
    p_quote.font.size = Pt(14)
    p_quote.font.italic = True
    p_quote.font.color.rgb = ACCENT_PURPLE

    # Right Column (Challenges & Solution)
    challenges = [
        ("1", "Local Framework Limitations", "LangGraph, CrewAI, and AutoGen are excellent for prototyping, but lack native cloud scaling, secure sandbox execution, and centralized policy control out-of-the-box.", ACCENT_CYAN),
        ("2", "Enterprise Requirements", "Organizations require secure session isolation, user authentication, auditing (observability), and strict authorization over what databases and tools an agent can call.", ACCENT_CYAN),
        ("★", "The Solution: AgentCore", "A fully managed, framework-agnostic platform specifically built to deploy and scale production agents with enterprise compliance.", ACCENT_PURPLE)
    ]

    for i, (num, title, desc, accent) in enumerate(challenges):
        top = Inches(1.8 + i * 1.6)
        card = create_card_shape(slide4, Inches(6.75), top, Inches(5.833), Inches(1.4), CARD_BG, BORDER_COLOR)
        if num == "★":
            card.line.color.rgb = ACCENT_PURPLE
        tf_card = card.text_frame
        
        p_c1 = tf_card.paragraphs[0]
        p_c1.text = f"[{num}]  {title}"
        p_c1.font.name = 'Arial'
        p_c1.font.size = Pt(14)
        p_c1.font.bold = True
        p_c1.font.color.rgb = accent
        p_c1.space_after = Pt(4)
        
        p_c2 = tf_card.add_paragraph()
        p_c2.text = desc
        p_c2.font.name = 'Arial'
        p_c2.font.size = Pt(11)
        p_c2.font.color.rgb = TEXT_MUTED

    add_speaker_notes(slide4, 
        "This slide sets up the problem statement. Why do we need AgentCore? "
        "Explain that while students can write an agent loop locally in 10 lines of Python, "
        "running that loop for 10,000 parallel enterprise users requires a managed cloud infrastructure.")

    # =========================================================================
    # SLIDE 5: AgentCore Architecture
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5)
    add_header(slide5, "Architectural Diagram", "Amazon Bedrock AgentCore Architecture")

    # Add Architecture Diagram Image
    image_path = "agentcore_architecture.png"
    slide5.shapes.add_picture(image_path, Inches(0.75), Inches(1.8), Inches(11.833), Inches(3.8))


    add_speaker_notes(slide5, 
        "Use this architecture slide to walk through the developer flow. "
        "A developer builds using Harness/CLI/SDK (second layer). "
        "The agent execution is powered by 10 modules (middle left) and deploys to Runtime (middle right). "
        "Finally, engineers assess and monitor using Observability & Evaluations at the bottom.")

    # =========================================================================
    # SLIDE 6: AgentCore Modules - Harness & Built-In Tools
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6)
    add_header(slide6, "AgentCore Modules • Build & Tools", "Harness & Built-In Tools")

    # Left Column: Harness & Built-in Tools
    left_box = slide6.shapes.add_textbox(Inches(0.75), Inches(1.8), Inches(5.5), Inches(4.5))
    tf6_left = left_box.text_frame
    tf6_left.word_wrap = True
    
    p_h = tf6_left.paragraphs[0]
    p_h.text = "🛠️ Harness"
    p_h.font.name = 'Arial'
    p_h.font.size = Pt(16)
    p_h.font.bold = True
    p_h.font.color.rgb = ACCENT_CYAN
    p_h.space_after = Pt(6)

    p_h_desc = tf6_left.add_paragraph()
    p_h_desc.text = "Harness offers a fully managed agent loop execution environment. It automatically orchestrates execution blocks, handling prompt-response cycles, routing tools, and managing state.\n• Gives each session an isolated container workspace with a filesystem.\n• Simply define model, system prompt, and tools list to activate."
    p_h_desc.font.name = 'Arial'
    p_h_desc.font.size = Pt(12)
    p_h_desc.font.color.rgb = TEXT_MUTED
    p_h_desc.space_after = Pt(20)

    p_t = tf6_left.add_paragraph()
    p_t.text = "📦 Built-in Tools"
    p_t.font.name = 'Arial'
    p_t.font.size = Pt(16)
    p_t.font.bold = True
    p_t.font.color.rgb = ACCENT_CYAN
    p_t.space_after = Pt(6)

    p_t_desc = tf6_left.add_paragraph()
    p_t_desc.text = "Provides secure integration of Amazon's managed tools directly into the agent context.\n• Secure Browser: Allows agents to safely search, click links, and browse pages.\n• Code Interpreter: Runs a secure, sandboxed Python runtime to calculate formulas, parse data files, and compile charts."
    p_t_desc.font.name = 'Arial'
    p_t_desc.font.size = Pt(12)
    p_t_desc.font.color.rgb = TEXT_MUTED

    # Right Column: CLI code block box
    cli_card = create_card_shape(slide6, Inches(6.75), Inches(1.8), Inches(5.833), Inches(4.5), CARD_BG, BORDER_COLOR)
    tf_cli = cli_card.text_frame
    
    p_c1 = tf_cli.paragraphs[0]
    p_c1.text = "AgentCore CLI command workflow:"
    p_c1.font.name = 'Arial'
    p_c1.font.size = Pt(14)
    p_c1.font.bold = True
    p_c1.font.color.rgb = ACCENT_PURPLE
    p_c1.space_after = Pt(12)
    
    p_code = tf_cli.add_paragraph()
    p_code.text = (
        "$ npm install -g @aws/agentcore\n"
        "✓ Installed AgentCore CLI v1.2.0\n\n"
        "$ agentcore init my-agent\n"
        "Initializing new agent skeleton...\n"
        "  - agent.json (Harness setup)\n"
        "  - prompt.txt (Instructions)\n\n"
        "$ agentcore deploy --harness\n"
        "Deploying my-agent to AWS Harness...\n"
        "🚀 Harness active! Endpoint:\n"
        "https://agentcore.us-east-1.amazonaws.com/harness/arn:..."
    )
    p_code.font.name = 'Courier New'
    p_code.font.size = Pt(11)
    p_code.font.color.rgb = TEXT_WHITE
    p_code.space_before = Pt(8)

    add_speaker_notes(slide6, 
        "Harness is the core logic manager. Explain that it does the heavy lifting of the 'agent loop'. "
        "Explain built-in tools: a Code Interpreter allows agents to execute arbitrary Python in a sandbox, "
        "and the Browser lets them fetch live content. These are essential for robust agent capabilities.")

    # =========================================================================
    # SLIDE 7: AgentCore Modules - Gateways & Secure Identity
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7)
    add_header(slide7, "AgentCore Modules • Core Connections", "Gateways & Secure Identity")

    # Left Column: Gateways
    left_card = create_card_shape(slide7, Inches(0.75), Inches(1.8), Inches(5.5), Inches(4.5), CARD_BG, ACCENT_PURPLE)
    tf_gw = left_card.text_frame
    p_g_t = tf_gw.paragraphs[0]
    p_g_t.text = "🔌 Gateways"
    p_g_t.font.name = 'Arial'
    p_g_t.font.size = Pt(18)
    p_g_t.font.bold = True
    p_g_t.font.color.rgb = ACCENT_PURPLE
    p_g_t.space_after = Pt(10)
    
    p_g_d = tf_gw.add_paragraph()
    p_g_d.text = (
        "Gateways use open source protocols, specifically the Model Context Protocol (MCP), "
        "to call external tools through OpenAPI schemas, REST APIs, or pre-configured integrations.\n\n"
        "• Eliminates the need to write custom middleware code or manage dedicated API routing infrastructure.\n\n"
        "• Integrates with security profiles to safely manage credentials and connection endpoints."
    )
    p_g_d.font.name = 'Arial'
    p_g_d.font.size = Pt(13)
    p_g_d.font.color.rgb = TEXT_MUTED

    # Right Column: Identity
    right_card = create_card_shape(slide7, Inches(6.75), Inches(1.8), Inches(5.833), Inches(4.5), CARD_BG, ACCENT_CYAN)
    tf_id = right_card.text_frame
    p_i_t = tf_id.paragraphs[0]
    p_i_t.text = "🔑 Identity (Inbound & Outbound)"
    p_i_t.font.name = 'Arial'
    p_i_t.font.size = Pt(18)
    p_i_t.font.bold = True
    p_i_t.font.color.rgb = ACCENT_CYAN
    p_i_t.space_after = Pt(10)
    
    p_i_d = tf_id.add_paragraph()
    p_i_d.text = (
        "Identity enables agents to securely manage resource access by integrating with standard enterprise identity providers (e.g. AWS IAM Identity Center).\n\n"
        "Inbound Identity:\n"
        "Verifies client caller credentials, authenticating that the user has permissions to invoke the agent session.\n\n"
        "Outbound Identity:\n"
        "Provides downstream resource access. Allows the agent to act on behalf of the user to access databases, databases, or third-party APIs using delegated permissions."
    )
    p_i_d.font.name = 'Arial'
    p_i_d.font.size = Pt(12)
    p_i_d.font.color.rgb = TEXT_MUTED

    add_speaker_notes(slide7, 
        "Gateways use the Model Context Protocol (MCP). Emphasize that MCP is the new open standard "
        "supported by Anthropic, AWS, and others. Inbound/Outbound identity is critical for corporate compliance. "
        "Ask: 'How does an agent write an email on behalf of a user? Outbound Identity delegation.'")

    # =========================================================================
    # SLIDE 8: AgentCore Modules - Memory & Policy Control
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide8)
    add_header(slide8, "AgentCore Modules • Context & Control", "Memory & Policy Control")

    # Left Column: Memory
    left_card = create_card_shape(slide8, Inches(0.75), Inches(1.8), Inches(5.5), Inches(4.5), CARD_BG, ACCENT_GOLD)
    tf_mem = left_card.text_frame
    p_m_t = tf_mem.paragraphs[0]
    p_m_t.text = "🧠 Memory & State Management"
    p_m_t.font.name = 'Arial'
    p_m_t.font.size = Pt(18)
    p_m_t.font.bold = True
    p_m_t.font.color.rgb = ACCENT_GOLD
    p_m_t.space_after = Pt(15)
    
    p_m_s1 = tf_mem.add_paragraph()
    p_m_s1.text = "Short-Term Memory:"
    p_m_s1.font.name = 'Arial'
    p_m_s1.font.size = Pt(13)
    p_m_s1.font.bold = True
    p_m_s1.font.color.rgb = TEXT_WHITE
    p_m_s2 = tf_mem.add_paragraph()
    p_m_s2.text = "Keeps track of conversation history within the current active session (e.g. current variables, task stack, step results)."
    p_m_s2.font.name = 'Arial'
    p_m_s2.font.size = Pt(11)
    p_m_s2.font.color.rgb = TEXT_MUTED
    p_m_s2.space_after = Pt(15)

    p_m_l1 = tf_mem.add_paragraph()
    p_m_l1.text = "Long-Term Memory:"
    p_m_l1.font.name = 'Arial'
    p_m_l1.font.size = Pt(13)
    p_m_l1.font.bold = True
    p_m_l1.font.color.rgb = TEXT_WHITE
    p_m_l2 = tf_mem.add_paragraph()
    p_m_l2.text = "Automatically extracts and archives facts, user preferences, and entity details across multiple historical sessions to provide context-aware responses."
    p_m_l2.font.name = 'Arial'
    p_m_l2.font.size = Pt(11)
    p_m_l2.font.color.rgb = TEXT_MUTED

    # Right Column: Policy
    right_card = create_card_shape(slide8, Inches(6.75), Inches(1.8), Inches(5.833), Inches(4.5), CARD_BG, ACCENT_PURPLE)
    tf_pol = right_card.text_frame
    p_p_t = tf_pol.paragraphs[0]
    p_p_t.text = "🛡️ Policy (Cedar Auth)"
    p_p_t.font.name = 'Arial'
    p_p_t.font.size = Pt(18)
    p_p_t.font.bold = True
    p_p_t.font.color.rgb = ACCENT_PURPLE
    p_p_t.space_after = Pt(10)
    
    p_p_d = tf_pol.add_paragraph()
    p_p_d.text = (
        "Policy offers deterministic control to ensure agents operate within defined boundaries. "
        "Author fine-grained rules using Cedar (AWS's open-source policy language) to prevent compliance failure.\n\n"
        "Example Cedar Snippet:"
    )
    p_p_d.font.name = 'Arial'
    p_p_d.font.size = Pt(12)
    p_p_d.font.color.rgb = TEXT_MUTED
    p_p_d.space_after = Pt(10)

    # Cedar Code
    p_code = tf_pol.add_paragraph()
    p_code.text = (
        "permit (\n"
        "    principal == User::\"Alice\",\n"
        "    action == Action::\"ReadAccountBalance\",\n"
        "    resource == Account::\"12345\"\n"
        ") when {\n"
        "    resource.region == \"US\"\n"
        "};"
    )
    p_code.font.name = 'Courier New'
    p_code.font.size = Pt(11)
    p_code.font.color.rgb = ACCENT_CYAN

    add_speaker_notes(slide8, 
        "Memory gives agents continuity. Policy engines like Cedar give them safety. "
        "Ask students: 'If the LLM has a prompt saying do not display account balance to non-US users, "
        "can it be jailbroken?' Yes. 'But if Cedar policy explicitly forbids it, can it be jailbroken?' "
        "No. Cedar policy checks are deterministic, checked by AWS before invoking the API.")

    # =========================================================================
    # SLIDE 9: AgentCore Modules - Registry & Runtime
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide9)
    add_header(slide9, "AgentCore Modules • Deployment & Sharing", "Registry & Runtime")

    # Left Column: Registry
    left_card = create_card_shape(slide9, Inches(0.75), Inches(1.8), Inches(5.5), Inches(4.5), CARD_BG, ACCENT_CYAN)
    tf_reg = left_card.text_frame
    p_r_t = tf_reg.paragraphs[0]
    p_r_t.text = "📂 Registry (Preview)"
    p_r_t.font.name = 'Arial'
    p_r_t.font.size = Pt(18)
    p_r_t.font.bold = True
    p_r_t.font.color.rgb = ACCENT_CYAN
    p_r_t.space_after = Pt(15)
    
    p_r_d = tf_reg.add_paragraph()
    p_r_d.text = (
        "Registry offers a centralized hub to publish, version, and reuse agentic assets across teams.\n\n"
        "• Asset Discovery: Easily publish and find existing agents, MCP servers, custom tools, and specific skill libraries.\n\n"
        "• Version Locking: Version control agentic assets so production clients remain locked to stable assets while development tests newer runs.\n\n"
        "• Code Reusability: Encourages teams to share custom tool implementations, preventing duplicate coding."
    )
    p_r_d.font.name = 'Arial'
    p_r_d.font.size = Pt(12)
    p_r_d.font.color.rgb = TEXT_MUTED

    # Right Column: Runtime
    right_card = create_card_shape(slide9, Inches(6.75), Inches(1.8), Inches(5.833), Inches(4.5), CARD_BG, ACCENT_PURPLE)
    tf_run = right_card.text_frame
    p_rn_t = tf_run.paragraphs[0]
    p_rn_t.text = "🚀 Runtime for Agents and Tools"
    p_rn_t.font.name = 'Arial'
    p_rn_t.font.size = Pt(18)
    p_rn_t.font.bold = True
    p_rn_t.font.color.rgb = ACCENT_PURPLE
    p_rn_t.space_after = Pt(15)
    
    p_rn_d = tf_run.add_paragraph()
    p_rn_d.text = (
        "Runtime is the secure, serverless engine that hosts and executes agent and tool code.\n\n"
        "• Fast Cold Starts: Tailored container configurations boot in under 50ms, maintaining response snappiness.\n\n"
        "• True Session Isolation: Each chat session runs inside its own sandbox boundary, guaranteeing data privacy.\n\n"
        "• Framework Agnostic: Deploy Python, JS, or Go codes natively. Scales up/down automatically to match query demands."
    )
    p_rn_d.font.name = 'Arial'
    p_rn_d.font.size = Pt(12)
    p_rn_d.font.color.rgb = TEXT_MUTED

    add_speaker_notes(slide9, 
        "Registry is like an 'npm registry' or 'docker hub' for agents and tools in a large company. "
        "Runtime is the actual compute engine, similar to AWS Lambda, but customized specifically "
        "to handle stateful agent loops, longer processing windows, and multimodal data payloads.")

    # =========================================================================
    # SLIDE 10: AgentCore Modules - Payments, Observability & Evaluations
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide10)
    add_header(slide10, "AgentCore Modules • Value & Assessment", "Payments, Observability & Evaluations")

    # Left Column: Payments
    left_card = create_card_shape(slide10, Inches(0.75), Inches(1.8), Inches(5.5), Inches(4.5), CARD_BG, ACCENT_GOLD)
    tf_pay = left_card.text_frame
    p_py_t = tf_pay.paragraphs[0]
    p_py_t.text = "💳 Payments"
    p_py_t.font.name = 'Arial'
    p_py_t.font.size = Pt(18)
    p_py_t.font.bold = True
    p_py_t.font.color.rgb = ACCENT_GOLD
    p_py_t.space_after = Pt(15)
    
    p_py_d = tf_pay.add_paragraph()
    p_py_d.text = (
        "Enables agents to autonomously execute micro-transaction payments for paid APIs, custom tools, or proprietary knowledge databases.\n\n"
        "• Secure Credentials: Wallets and API credentials are kept encrypted and managed safely under AgentCore Identity.\n\n"
        "• Micro-budgeting: Authorize agents to spend small budgets to solve complex sub-tasks, facilitating agent-to-agent economics."
    )
    p_py_d.font.name = 'Arial'
    p_py_d.font.size = Pt(13)
    p_py_d.font.color.rgb = TEXT_MUTED

    # Right Column: Observability & Evaluations
    right_card = create_card_shape(slide10, Inches(6.75), Inches(1.8), Inches(5.833), Inches(4.5), CARD_BG, ACCENT_CYAN)
    tf_oe = right_card.text_frame
    p_oe_t = tf_oe.paragraphs[0]
    p_oe_t.text = "📊 Observability & Evaluations"
    p_oe_t.font.name = 'Arial'
    p_oe_t.font.size = Pt(18)
    p_oe_t.font.bold = True
    p_oe_t.font.color.rgb = ACCENT_CYAN
    p_oe_t.space_after = Pt(15)
    
    p_oe_d = tf_oe.add_paragraph()
    p_oe_d.text = (
        "Ensures engineering teams can trace, debug, and validate production agent behavior over time.\n\n"
        "Observability:\n"
        "Generates thorough trace logs showing the agent's exact reasoning paths, tool invocation details, arguments, and return variables.\n\n"
        "Evaluations:\n"
        "Configure automated batch test suits or online evaluators to audit prompt adjustments and prevent regressions before deploying code changes."
    )
    p_oe_d.font.name = 'Arial'
    p_oe_d.font.size = Pt(12)
    p_oe_d.font.color.rgb = TEXT_MUTED

    add_speaker_notes(slide10, 
        "Payments is a unique capability: agents having wallets to make microtransactions. "
        "Observability/Evaluations is about maintaining quality control. Traces show *why* an agent made a decision, "
        "and Evaluations test prompt updates against safety benchmarks.")

    # =========================================================================
    # SLIDE 11: Comparison Table
    # =========================================================================
    slide11 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide11)
    add_header(slide11, "Comparative Analysis", "Amazon Bedrock Agents vs. AgentCore")

    # Add a Native Table Shape
    rows = 7
    cols = 3
    table_shape = slide11.shapes.add_table(rows, cols, Inches(0.75), Inches(1.8), Inches(11.833), Inches(4.8))
    table = table_shape.table

    # Column Widths
    table.columns[0].width = Inches(2.2)
    table.columns[1].width = Inches(4.8)
    table.columns[2].width = Inches(4.833)

    headers = ["Dimension", "Amazon Bedrock Agents (Classic)", "Amazon Bedrock AgentCore"]
    for c, text in enumerate(headers):
        cell = table.cell(0, c)
        cell.text = text
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(15, 23, 42)
        p = cell.text_frame.paragraphs[0]
        p.font.name = 'Arial'
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = ACCENT_CYAN

    data = [
        ("Primary Focus", "Simple, low-code AWS-native agent builder.", "Managed platform/runtime to deploy and scale any agent code."),
        ("Framework Support", "Locked to Amazon's proprietary orchestration loop.", "Framework Agnostic (LangGraph, CrewAI, AutoGen, custom code)."),
        ("Model Agnosticism", "Optimized for Bedrock-native models (Claude, Titan).", "Model Agnostic (Supports external models, custom weights)."),
        ("Extensibility", "Requires AWS Lambda action groups.", "Supports Model Context Protocol (MCP) and sandboxed runtimes."),
        ("Session Memory", "Managed session attributes (ephemeral).", "Automated Short & Long term memory across multiple sessions."),
        ("Security Control", "AWS IAM roles per agent.", "Granular Cedar Policy authorization + Inbound/Outbound identity.")
    ]

    for r, row_data in enumerate(data):
        for c, text in enumerate(row_data):
            cell = table.cell(r + 1, c)
            cell.text = text
            cell.fill.solid()
            # Alternating background colors
            if (r + 1) % 2 == 0:
                cell.fill.fore_color.rgb = RGBColor(12, 18, 30)
            else:
                cell.fill.fore_color.rgb = RGBColor(7, 11, 19)
            
            p = cell.text_frame.paragraphs[0]
            p.font.name = 'Arial'
            p.font.size = Pt(10.5)
            p.font.color.rgb = TEXT_WHITE if c == 2 else TEXT_MUTED
            if c == 0:
                p.font.bold = True
                p.font.color.rgb = ACCENT_CYAN

    add_speaker_notes(slide11, 
        "Make sure the comparison is clear. Bedrock Agents (Classic) is a specific low-code builder "
        "that uses Bedrock models and Lambdas. Bedrock AgentCore is the newer, broader enterprise platform "
        "that allows you to take *any* custom agent code (written in LangGraph or python) and run/scale it "
        "with enterprise memory, identity, policy, and payments.")

    # =========================================================================
    # SLIDE 12: Discussion & Summary
    # =========================================================================
    slide12 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide12)
    add_header(slide12, "Class Discussion & Practice", "Review & Discussion Points")

    # Left Column: Discussion Questions
    left_box = slide12.shapes.add_textbox(Inches(0.75), Inches(1.8), Inches(5.5), Inches(4.5))
    tf12_left = left_box.text_frame
    tf12_left.word_wrap = True
    
    p_disc = tf12_left.paragraphs[0]
    p_disc.text = "Key Lecture Discussion Topics:"
    p_disc.font.name = 'Arial'
    p_disc.font.size = Pt(16)
    p_disc.font.bold = True
    p_disc.font.color.rgb = ACCENT_GOLD
    p_disc.space_after = Pt(15)

    questions = [
        ("1. Multi-Agent Collaboration", "How does the AgentCore Registry facilitate teams building specialized agents that collaborate using open protocols like MCP?"),
        ("2. Outbound Identity delegation", "Under what scenarios is Outbound Identity essential? (e.g. accessing a customer's personal corporate calendar or order database)."),
        ("3. Compliance & Cedar Policies", "Why should developers rely on deterministic policy files (Cedar) instead of writing safety guidelines in natural language system prompts?")
    ]

    for q_title, q_desc in questions:
        p_q_t = tf12_left.add_paragraph()
        p_q_t.text = q_title
        p_q_t.font.name = 'Arial'
        p_q_t.font.size = Pt(12)
        p_q_t.font.bold = True
        p_q_t.font.color.rgb = TEXT_WHITE
        p_q_t.space_before = Pt(10)
        
        p_q_d = tf12_left.add_paragraph()
        p_q_d.text = q_desc
        p_q_d.font.name = 'Arial'
        p_q_d.font.size = Pt(10.5)
        p_q_d.font.color.rgb = TEXT_MUTED

    # Right Column: Summary Card
    summary_card = create_card_shape(slide12, Inches(6.75), Inches(1.8), Inches(5.833), Inches(4.5), CARD_BG, BORDER_COLOR)
    summary_card.line.color.rgb = ACCENT_PURPLE
    tf_sum = summary_card.text_frame
    
    p_s_t = tf_sum.paragraphs[0]
    p_s_t.text = "Lecture Summary"
    p_s_t.font.name = 'Arial'
    p_s_t.font.size = Pt(18)
    p_s_t.font.bold = True
    p_s_t.font.color.rgb = ACCENT_PURPLE
    p_s_t.space_after = Pt(15)
    
    summary_points = [
        "AWS Bedrock: Unified API for foundation models (Claude, Llama, Titan) + customizations (fine-tuning, knowledge bases, guardrails).",
        "AgentCore Harness/CLI/SDK: Connection frameworks allowing developers to build locally first.",
        "AgentCore Modules: 10 middleware modules (Memory, Identity, Policy, Gateways, registry, payments) that handle enterprise operations.",
        "AgentCore Runtime: Serverless, purpose-built execution environment for isolated scaling."
    ]
    for pt in summary_points:
        p_pt = tf_sum.add_paragraph()
        p_pt.text = "• " + pt
        p_pt.font.name = 'Arial'
        p_pt.font.size = Pt(11)
        p_pt.font.color.rgb = TEXT_MUTED
        p_pt.space_before = Pt(8)

    add_speaker_notes(slide12, 
        "Use this final slide to wrap up the lecture and transition to the lab work. "
        "Reiterate that probabilistic AI needs deterministic cloud compliance parameters (Cedar, Outbound Identity) "
        "to run securely in enterprise systems. Prepare students for the hand-on workshop using AgentCore CLI next.")

    # Save Presentation
    output_filename = "AWS_Bedrock_and_AgentCore_Presentation.pptx"
    prs.save(output_filename)
    print(f"Presentation saved successfully as '{output_filename}'")

if __name__ == "__main__":
    create_presentation()
