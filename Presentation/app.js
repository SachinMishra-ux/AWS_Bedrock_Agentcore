/**
 * AWS Bedrock & AgentCore Presentation (app.js)
 * Logic: Navigation, Keyboard controls, SVG clicks, Accordions, Terminal Simulation, Fullscreen
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. DOM Elements
    const slides = document.querySelectorAll('.slide');
    const navItems = document.querySelectorAll('.nav-item');
    const progressBar = document.getElementById('progress-bar');
    const currentSlideNum = document.getElementById('current-slide-num');
    const totalSlidesNum = document.getElementById('total-slides-num');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    const fullscreenBtn = document.getElementById('fullscreen-btn');
    
    const sidebar = document.getElementById('sidebar');
    const hideSidebarBtn = document.getElementById('hide-sidebar-btn');
    const showSidebarBtn = document.getElementById('show-sidebar-btn');
    
    const detailModal = document.getElementById('detail-modal');
    const modalCloseBtn = document.getElementById('modal-close-btn');
    const modalBodyContent = document.getElementById('modal-body-content');
    
    const runTerminalBtn = document.getElementById('run-terminal-btn');
    const cliTerminal = document.getElementById('cli-terminal');

    // 2. Navigation State
    let currentSlide = 0;
    const totalSlides = slides.length;
    totalSlidesNum.textContent = totalSlides;

    // 3. Navigation Functions
    function updateSlide(index) {
        // Enforce boundaries
        if (index < 0) index = 0;
        if (index >= totalSlides) index = totalSlides - 1;
        
        currentSlide = index;

        // Active classes for slides
        slides.forEach((slide, idx) => {
            if (idx === index) {
                slide.classList.add('active');
            } else {
                slide.classList.remove('active');
            }
        });

        // Active classes for sidebar navigation
        navItems.forEach((item) => {
            const itemIdx = parseInt(item.getAttribute('data-slide'));
            if (itemIdx === index) {
                item.classList.add('active');
                item.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            } else {
                item.classList.remove('active');
            }
        });

        // Progress bar
        const progressPercent = (index / (totalSlides - 1)) * 100;
        progressBar.style.width = `${progressPercent}%`;

        // Slide numbers
        currentSlideNum.textContent = index + 1;
    }

    function nextSlide() {
        if (currentSlide < totalSlides - 1) {
            updateSlide(currentSlide + 1);
        }
    }

    function prevSlide() {
        if (currentSlide > 0) {
            updateSlide(currentSlide - 1);
        }
    }

    // 4. Event Listeners (Navigation)
    prevBtn.addEventListener('click', prevSlide);
    nextBtn.addEventListener('click', nextSlide);

    navItems.forEach((item) => {
        item.addEventListener('click', () => {
            const index = parseInt(item.getAttribute('data-slide'));
            updateSlide(index);
        });
    });

    // Keyboard Shortcuts
    document.addEventListener('keydown', (e) => {
        // Skip keys if modal is open to avoid double inputs
        if (!detailModal.classList.contains('hidden')) {
            if (e.key === 'Escape') {
                closeModal();
            }
            return;
        }

        switch (e.key) {
            case 'ArrowRight':
            case ' ':
            case 'PageDown':
                e.preventDefault();
                nextSlide();
                break;
            case 'ArrowLeft':
            case 'PageUp':
                e.preventDefault();
                prevSlide();
                break;
            case 'Home':
                e.preventDefault();
                updateSlide(0);
                break;
            case 'End':
                e.preventDefault();
                updateSlide(totalSlides - 1);
                break;
        }
    });

    // 5. Sidebar Toggle Actions
    hideSidebarBtn.addEventListener('click', () => {
        sidebar.classList.add('collapsed');
        showSidebarBtn.classList.remove('hidden');
    });

    showSidebarBtn.addEventListener('click', () => {
        sidebar.classList.remove('collapsed');
        showSidebarBtn.classList.add('hidden');
    });

    // 6. Fullscreen Mode
    fullscreenBtn.addEventListener('click', () => {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen().catch(err => {
                console.error(`Error enabling fullscreen: ${err.message}`);
            });
        } else {
            document.exitFullscreen();
        }
    });

    // 7. Accordion Toggle Logic (Slide 6)
    const accordionHeaders = document.querySelectorAll('.accordion-header');
    accordionHeaders.forEach(header => {
        header.addEventListener('click', () => {
            const parent = header.parentElement;
            const wasActive = parent.classList.contains('active');
            
            // Close all items
            document.querySelectorAll('.accordion-item').forEach(item => {
                item.classList.remove('active');
            });

            // Toggle clicked item
            if (!wasActive) {
                parent.classList.add('active');
            }
        });
    });

    // 8. Dynamic Modal Details (Slide 5 Architecture Clicks)
    const layerData = {
        'agent-layer': {
            title: 'Agent Layer',
            badge: 'Framework & Model Agnostic Client',
            description: 'The outermost layer of the application where agentic execution flows. Developers are not restricted to AWS frameworks and can choose standard packages for the agent loop.',
            bullets: [
                '<strong>Any Framework:</strong> Seamless support for LangGraph, CrewAI, AutoGen, Strands, or direct custom loops.',
                '<strong>Any Model:</strong> Connect agents to Claude 3.5, Llama 3, Amazon Titan, or even proprietary models hosted on custom endpoints.',
                '<strong>Any Protocol:</strong> Uses Model Context Protocol (MCP) or standard REST APIs to exchange messages and tools.'
            ]
        },
        'build-layer': {
            title: 'Harness • CLI • SDK',
            badge: 'Development Toolchain',
            description: 'Tools that help engineers write, configure, and compile agent bundles locally before securely deploying them to the cloud.',
            bullets: [
                '<strong>AgentCore Harness:</strong> The orchestrator loop that manages variables, loads prompt templates, and links modules together automatically.',
                '<strong>AgentCore CLI:</strong> Developer command-line tool (`@aws/agentcore`) to bootstrap projects, sync schemas, run dry tests, and execute deploys.',
                '<strong>AgentCore SDK:</strong> Python and Node.js SDKs providing high-level functions to invoke the Harness loop and interact with state.'
            ]
        },
        'modules-layer': {
            title: 'AgentCore Service Modules',
            badge: '10 Core Architecture Primitives',
            description: 'The horizontal suite of components managing complexity for production-ready agents.',
            bullets: [
                '<strong>Built-in Tools:</strong> Secure, sandboxed Web Browsing and Python Code Interpreter.',
                '<strong>Gateway:</strong> Handles connection to REST/OpenAPI and Model Context Protocol (MCP) servers without writing extra routes.',
                '<strong>Identity & Policy:</strong> Enforces IAM-based authorization and Cedar policy checks for secure calls.',
                '<strong>Memory & Registry:</strong> Retains session state and registers reusable tools, skills, and agents across teams.',
                '<strong>Payments:</strong> Manages credential budgets to pay for external premium API microtransactions.'
            ]
        },
        'runtime-layer': {
            title: 'AgentCore Runtime',
            badge: 'Secure Serverless Infrastructure',
            description: 'The execution layer of AgentCore. Unlike generic serverless platforms, Runtime is custom-tailored for the resource and scaling needs of AI agents.',
            bullets: [
                '<strong>Zero Infrastructure:</strong> Runs serverless containers with extremely fast cold starts (< 50ms).',
                '<strong>Isolation Boundary:</strong> Every agent session has its own sandboxed execution shell with local file write permissions.',
                '<strong>Multi-Modal & Long Executions:</strong> Designed to process large payloads (images, video, tables) and support long-lived polling loops without timeouts.'
            ]
        },
        'assess-layer': {
            title: 'Observability & Evaluations',
            badge: 'Monitoring, Testing & Compliance',
            description: 'Provides deep visibility into agent decision paths, tool parameters, and response evaluations to prevent errors in production.',
            bullets: [
                '<strong>Observability Traces:</strong> Tracks exact steps, showing which tools were triggered, input arguments, and prompt histories.',
                '<strong>Batch Evaluations:</strong> Runs automated validation suites to test response accuracy and latency against test datasets.',
                '<strong>Custom Evaluators:</strong> Allows deploying dedicated models or guardrails to continuously grade live session conversations.'
            ]
        }
    };

    window.showModuleDetail = function(layerKey) {
        const data = layerData[layerKey];
        if (!data) return;

        let bulletsHtml = data.bullets.map(b => `<li>${b}</li>`).join('');
        
        modalBodyContent.innerHTML = `
            <span class="modal-badge">${data.badge}</span>
            <h3>${data.title}</h3>
            <p>${data.description}</p>
            <ul>${bulletsHtml}</ul>
            <button class="btn btn-cyan" onclick="closeModal()">Close Details</button>
        `;
        
        detailModal.classList.remove('hidden');
    };

    function closeModal() {
        detailModal.classList.add('hidden');
    }

    modalCloseBtn.addEventListener('click', closeModal);
    detailModal.addEventListener('click', (e) => {
        if (e.target === detailModal) {
            closeModal();
        }
    });

    window.closeModal = closeModal; // Export to global namespace

    // 9. Mock Terminal Simulator (Slide 6)
    let isSimulating = false;
    
    function simulateTerminal() {
        if (isSimulating) return;
        isSimulating = true;
        runTerminalBtn.disabled = true;
        
        cliTerminal.innerHTML = '';
        
        const lines = [
            { text: '$ npm install -g @aws/agentcore', type: 'cmd', delay: 400 },
            { text: '✓ Installed AgentCore CLI v1.2.0 (148 packages)', type: 'ok', delay: 800 },
            { text: '$ agentcore init travel-agent', type: 'cmd', delay: 600 },
            { text: 'Creating skeleton repository inside ./travel-agent...', type: 'text', delay: 400 },
            { text: '  - agent.json (Harness setup)', type: 'indent', delay: 200 },
            { text: '  - instructions.md (System Prompts)', type: 'indent', delay: 200 },
            { text: '  - tools/mcp-server.json (MCP Gateways)', type: 'indent', delay: 200 },
            { text: '$ agentcore test --local', type: 'cmd', delay: 600 },
            { text: '⚡ Running local simulation...', type: 'text', delay: 300 },
            { text: '  [Harness] Model: anthropic.claude-3-5-sonnet', type: 'indent', delay: 250 },
            { text: '  [Memory] Initialized local short-term session', type: 'indent', delay: 250 },
            { text: '  [Tools] Loaded 2 custom schemas & 1 MCP Server', type: 'indent', delay: 250 },
            { text: '✓ Simulation Success: Agent loop completes cleanly.', type: 'ok', delay: 400 },
            { text: '$ agentcore deploy --harness', type: 'cmd', delay: 800 },
            { text: '⚙ Creating cloud resources...', type: 'loading', delay: 500 },
            { text: '⚙ Connecting Outbound Identity roles...', type: 'loading', delay: 400 },
            { text: '🚀 Deployment Succeeded!', type: 'success', delay: 300 },
            { text: 'Harness Endpoint Active: https://agentcore.us-east-1.amazonaws.com/harness/arn:aws:bedrock:us-east-1:12345:agent/travel-agent-prod', type: 'text', delay: 100 }
        ];

        let index = 0;
        
        function printNextLine() {
            if (index < lines.length) {
                const lineInfo = lines[index];
                const div = document.createElement('div');
                
                if (lineInfo.type === 'cmd') {
                    div.className = 'line';
                    div.innerHTML = `<span class="cmd-prompt">$</span> ${lineInfo.text.replace('$ ', '')}`;
                } else if (lineInfo.type === 'ok') {
                    div.className = 'line ok';
                    div.textContent = lineInfo.text;
                } else if (lineInfo.type === 'success') {
                    div.className = 'line success';
                    div.textContent = lineInfo.text;
                } else if (lineInfo.type === 'loading') {
                    div.className = 'line loading';
                    div.textContent = lineInfo.text;
                } else if (lineInfo.type === 'indent') {
                    div.className = 'line-indent';
                    div.textContent = lineInfo.text;
                } else {
                    div.className = 'line';
                    div.textContent = lineInfo.text;
                }
                
                cliTerminal.appendChild(div);
                cliTerminal.scrollTop = cliTerminal.scrollHeight;
                
                index++;
                setTimeout(printNextLine, lineInfo.delay);
            } else {
                isSimulating = false;
                runTerminalBtn.disabled = false;
            }
        }

        printNextLine();
    }

    runTerminalBtn.addEventListener('click', simulateTerminal);
    
    // Auto-scroll sidebar layout elements
    updateSlide(0);
});
