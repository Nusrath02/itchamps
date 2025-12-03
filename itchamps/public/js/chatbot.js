// ITChamps AI Chatbot - Frontend (Enhanced Version)
(function() {
    // Prevent double initialization
    if (window.itchampsChatlbotInitialized) return;
    window.itchampsChatlbotInitialized = true;

    console.log('ITChamps Chatbot initializing...');

    // Remove any existing chatbot buttons from other apps
    setTimeout(function() {
        const existingBots = document.querySelectorAll('[class*="chatbot"], [id*="chatbot"], .widget-chatbot');
        existingBots.forEach(function(bot) {
            if (!bot.id || !bot.id.includes('itchamps')) {
                bot.style.display = 'none';
            }
        });
    }, 2000);

    // Add CSS styles (ENHANCED)
    const style = document.createElement('style');
    style.innerHTML = `
        /* Chatbot Dropdown Container */
        .chatbot-dropdown {
            display: none;
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 680px;
            max-width: 90vw;
            height: 600px;
            max-height: 85vh;
            background: #ffffff;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            border: 1px solid #e5e7eb;
            z-index: 9999;
            flex-direction: column;
            overflow: hidden;
            animation: slideDown 0.3s ease-out;
        }
        
        .chatbot-dropdown.active {
            display: flex;
        }
        
        @keyframes slideDown {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .chatbot-header {
            background: linear-gradient(90deg, #2563eb 0%, #3b82f6 100%) !important;
            padding: 16px 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-weight: 600;
            font-size: 18px;
            color: white;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }

        .chatbot-header-title {
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 20px;
        }

        .chatbot-header-title .chatbot-icon {
            font-size: 28px;
        }
        
        .chatbot-close-btn {
            background: rgba(255, 255, 255, 0.2);
            border: none;
            color: white;
            font-size: 24px;
            cursor: pointer;
            width: 36px;
            height: 36px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 8px;
            transition: all 0.2s;
            padding: 0;
        }
        
        .chatbot-close-btn:hover {
            background: rgba(255, 255, 255, 0.3);
        }
        
        .chatbot-messages {
            flex: 1;
            padding: 24px;
            overflow-y: auto;
            background: #f3f4f6;
        }
        
        .chatbot-messages::-webkit-scrollbar {
            width: 6px;
        }
        
        .chatbot-messages::-webkit-scrollbar-thumb {
            background: #cbd5e0;
            border-radius: 3px;
        }
        
        .chat-msg {
            margin-bottom: 20px;
            animation: fadeIn 0.3s ease-in;
            clear: both;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .chat-msg.user .msg-bubble {
            background: linear-gradient(135deg, rgb(30, 60, 114) 0%, rgb(42, 82, 152) 50%, rgb(79, 172, 254) 100%) !important;
            color: white;
            display: inline-block;
            padding: 12px 16px;
            border-radius: 18px 18px 4px 18px;
            max-width: 80%;
            word-wrap: break-word;
            float: right;
            font-size: 15px;
            line-height: 1.5;
            box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
        }

        .chat-msg.bot .msg-bubble {
            background: white;
            color: #374151;
            display: inline-block;
            padding: 16px 20px;
            border-radius: 20px;
            max-width: 85%;
            word-wrap: break-word;
            border: none;
            font-size: 15px;
            line-height: 1.6;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }
        
        /* Enhanced Markdown Styling */
        .msg-bubble h1,
        .msg-bubble h2 {
            font-size: 18px;
            font-weight: 700;
            color: #1a202c;
            margin: 16px 0 12px 0;
            padding-bottom: 8px;
            border-bottom: 2px solid #e2e8f0;
        }
        
        .msg-bubble h1:first-child,
        .msg-bubble h2:first-child {
            margin-top: 0;
        }
        
        .msg-bubble h3 {
            font-size: 16px;
            font-weight: 600;
            color: #2d3748;
            margin: 14px 0 10px 0;
        }
        
        .msg-bubble p {
            margin: 10px 0;
            color: #4a5568;
        }
        
        .msg-bubble ul,
        .msg-bubble ol {
            margin: 12px 0;
            padding-left: 24px;
        }
        
        .msg-bubble li {
            margin: 8px 0;
            color: #4a5568;
            line-height: 1.6;
        }
        
        .msg-bubble strong {
            font-weight: 600;
            color: #2d3748;
        }
        
        .msg-bubble code {
            background: #f7fafc;
            border: 1px solid #e2e8f0;
            border-radius: 4px;
            padding: 2px 6px;
            font-family: 'Courier New', monospace;
            font-size: 13px;
            color: #e53e3e;
        }
        
        .msg-bubble pre {
            background: #2d3748;
            color: #e2e8f0;
            padding: 12px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 12px 0;
        }
        
        .msg-bubble pre code {
            background: none;
            border: none;
            color: #e2e8f0;
            padding: 0;
        }
        
        .msg-bubble a {
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
        }
        
        .msg-bubble a:hover {
            text-decoration: underline;
        }
        
        .msg-bubble blockquote {
            border-left: 4px solid #667eea;
            padding-left: 16px;
            margin: 12px 0;
            color: #4a5568;
            font-style: italic;
        }
        
        .chatbot-input-area {
            display: flex;
            padding: 20px;
            background: white;
            border-top: 1px solid #e5e7eb;
            gap: 12px;
            align-items: center;
        }

        .chatbot-input-area input {
            flex: 1;
            border: 2px solid #d1d5db;
            outline: none;
            background: white;
            color: #374151;
            padding: 14px 20px;
            border-radius: 28px;
            font-size: 15px;
            transition: all 0.2s;
        }

        .chatbot-input-area input::placeholder {
            color: #9ca3af;
        }

        .chatbot-input-area input:focus {
            border-color: #3b82f6;
            background: white;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }

        .chatbot-input-area button {
            background: linear-gradient(90deg, #2563eb 0%, #3b82f6 100%) !important;
            color: white;
            border: none;
            padding: 14px 32px;
            border-radius: 28px;
            cursor: pointer;
            transition: all 0.2s;
            font-weight: 600;
            font-size: 15px;
            box-shadow: 0 2px 8px rgba(37, 99, 235, 0.3);
        }

        .chatbot-input-area button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
        }

        .chatbot-input-area button:active {
            transform: translateY(0);
        }
        
        /* Floating chatbot button */
        .chatbot-float-btn {
            position: fixed;
            bottom: 30px;
            right: 30px;
            width: 64px;
            height: 64px;
            background: linear-gradient(90deg, #2563eb 0%, #3b82f6 100%) !important;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            box-shadow: 0 8px 24px rgba(37, 99, 235, 0.4);
            z-index: 9998;
            font-size: 32px;
            transition: all 0.3s ease;
        }

        .chatbot-float-btn:hover {
            transform: scale(1.1);
            box-shadow: 0 12px 32px rgba(37, 99, 235, 0.5);
        }
        
        /* Overlay */
        .chatbot-overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 9998;
            background: rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(2px);
        }

        .chatbot-overlay.active {
            display: block;
        }
        
        /* Loading animation */
        .typing-indicator {
            display: inline-flex;
            gap: 4px;
            padding: 8px 0;
        }
        
        .typing-indicator span {
            width: 8px;
            height: 8px;
            background: #cbd5e0;
            border-radius: 50%;
            animation: typing 1.4s infinite;
        }
        
        .typing-indicator span:nth-child(2) {
            animation-delay: 0.2s;
        }
        
        .typing-indicator span:nth-child(3) {
            animation-delay: 0.4s;
        }
        
        @keyframes typing {
            0%, 60%, 100% { transform: translateY(0); }
            30% { transform: translateY(-10px); }
        }
    `;
    document.head.appendChild(style);

    // ENHANCED Markdown parser with all features
    function parseMarkdown(text) {
        // Escape HTML first
        text = text.replace(/&/g, '&amp;')
                   .replace(/</g, '&lt;')
                   .replace(/>/g, '&gt;');
        
        // Headers
        text = text.replace(/^### (.*$)/gim, '<h3>$1</h3>');
        text = text.replace(/^## (.*$)/gim, '<h2>$1</h2>');
        text = text.replace(/^# (.*$)/gim, '<h1>$1</h1>');
        
        // Bold
        text = text.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
        
        // Code blocks (before inline code)
        text = text.replace(/```([^`]+)```/g, '<pre><code>$1</code></pre>');
        
        // Inline code
        text = text.replace(/`([^`]+)`/g, '<code>$1</code>');
        
        // Links
        text = text.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank">$1</a>');
        
        // Lists
        text = text.replace(/^\* (.+)$/gim, '<li>$1</li>');
        text = text.replace(/^- (.+)$/gim, '<li>$1</li>');
        text = text.replace(/^\d+\. (.+)$/gim, '<li>$1</li>');
        
        // Wrap lists
        text = text.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');
        
        // Blockquotes
        text = text.replace(/^&gt; (.+)$/gim, '<blockquote>$1</blockquote>');
        
        // Paragraphs
        text = text.replace(/\n\n/g, '</p><p>');
        text = '<p>' + text + '</p>';
        
        // Clean up empty paragraphs
        text = text.replace(/<p><\/p>/g, '');
        text = text.replace(/<p>(<h[123]>)/g, '$1');
        text = text.replace(/(<\/h[123]>)<\/p>/g, '$1');
        text = text.replace(/<p>(<ul>)/g, '$1');
        text = text.replace(/(<\/ul>)<\/p>/g, '$1');
        text = text.replace(/<p>(<pre>)/g, '$1');
        text = text.replace(/(<\/pre>)<\/p>/g, '$1');
        text = text.replace(/<p>(<blockquote>)/g, '$1');
        text = text.replace(/(<\/blockquote>)<\/p>/g, '$1');
        
        return text;
    }

    // Create chatbot HTML
    const chatbotHTML = `
        <div class="chatbot-overlay" id="itchampsChatlbotOverlay"></div>

        <div class="chatbot-dropdown" id="itchampsChatlbotDropdown">
            <div class="chatbot-header">
                <div class="chatbot-header-title">
                    <span class="chatbot-icon">🤖</span>
                    <span>AI Assistant</span>
                </div>
                <button class="chatbot-close-btn" id="itchampsChatlbotCloseBtn" title="Close and Clear Chat">×</button>
            </div>
            <div class="chatbot-messages" id="itchampsChatlbotMessages"></div>
            <div class="chatbot-input-area">
                <input type="text" id="itchampsChatlbotInput" placeholder="Ask me anything..." />
                <button id="itchampsChatlbotSendBtn">Send</button>
            </div>
        </div>

        <div class="chatbot-float-btn" id="itchampsChatlbotFloatBtn" style="z-index: 10000 !important;" title="Open ITChamps AI Assistant">
            🤖
        </div>
    `;

    const div = document.createElement('div');
    div.id = 'itchamps-chatbot-container';
    div.innerHTML = chatbotHTML;
    document.body.appendChild(div);

    // Get elements
    const dropdown = document.getElementById('itchampsChatlbotDropdown');
    const overlay = document.getElementById('itchampsChatlbotOverlay');
    const closeBtn = document.getElementById('itchampsChatlbotCloseBtn');
    const floatBtn = document.getElementById('itchampsChatlbotFloatBtn');
    const input = document.getElementById('itchampsChatlbotInput');
    const sendBtn = document.getElementById('itchampsChatlbotSendBtn');
    const messages = document.getElementById('itchampsChatlbotMessages');

    // NEW: Render initial welcome messages
    function renderInitialMessages() {
        if (!messages) return;

        const introMessage = "👋 Hi! I'm your AI assistant. How can I help you today?";

        messages.innerHTML = `
            <div class="chat-msg bot">
                <div class="msg-bubble">${introMessage}</div>
            </div>
        `;
    }

    // Initialize with welcome messages
    renderInitialMessages();

    // Send message function
    window.sendMessage = async function() {
        const userMsg = input.value.trim();
        if (!userMsg) return;

        console.log('Sending message:', userMsg);

        const escapedMsg = userMsg.replace(/&/g, '&amp;')
                                  .replace(/</g, '&lt;')
                                  .replace(/>/g, '&gt;');

        messages.innerHTML += `
            <div class="chat-msg user">
                <div class="msg-bubble">${escapedMsg}</div>
            </div>
        `;
        input.value = '';

        messages.innerHTML += `
            <div class="chat-msg bot" id="itchampsChatlbotLoading">
                <div class="msg-bubble">
                    <div class="typing-indicator">
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>
                </div>
            </div>
        `;
        messages.scrollTop = messages.scrollHeight;

        try {
            const response = await frappe.call({
                method: 'itchamps.api.chatbot.get_response',
                args: { message: userMsg }
            });

            const loading = document.getElementById('itchampsChatlbotLoading');
            if (loading) loading.remove();

            const botMsg = response.message?.message || "Sorry, I couldn't process that.";
            const formattedMsg = parseMarkdown(botMsg);

            messages.innerHTML += `
                <div class="chat-msg bot">
                    <div class="msg-bubble">${formattedMsg}</div>
                </div>
            `;
        } catch (error) {
            const loading = document.getElementById('itchampsChatlbotLoading');
            if (loading) loading.remove();
            
            const errorMsg = error.message.replace(/&/g, '&amp;')
                                         .replace(/</g, '&lt;')
                                         .replace(/>/g, '&gt;');
            
            messages.innerHTML += `
                <div class="chat-msg bot">
                    <div class="msg-bubble" style="color: #e53e3e; border-color: #feb2b2;">
                        ⚠️ <strong>Error:</strong> ${errorMsg}
                    </div>
                </div>
            `;
            console.error('Chatbot error:', error);
        }

        messages.scrollTop = messages.scrollHeight;
        input.focus();
    };

    // NEW: Open chatbot (just show)
    window.openChatbot = function() {
        dropdown.classList.add('active');
        overlay.classList.add('active');
        setTimeout(() => input && input.focus(), 100);
        console.log('Chatbot opened');
    };

    // NEW: Close chatbot (just hide, keep history)
    window.closeChatbot = function() {
        dropdown.classList.remove('active');
        overlay.classList.remove('active');
        console.log('Chatbot closed');
    };

    // NEW: Close and clear chatbot (for X button)
    window.closeChatbotAndClear = function() {
        dropdown.classList.remove('active');
        overlay.classList.remove('active');
        
        // Clear chat messages and restore welcome message
        renderInitialMessages();
        
        console.log('Chatbot closed and cleared');
    };

    // Toggle chatbot
    window.toggleChatbot = function() {
        if (dropdown.classList.contains('active')) {
            closeChatbot();  // Just hide, don't clear
        } else {
            openChatbot();
        }
    };

    // Event listeners - UPDATED
    if (closeBtn) closeBtn.onclick = closeChatbotAndClear;  // X button clears chat
    if (overlay) overlay.onclick = closeChatbot;  // Overlay click just hides
    if (floatBtn) floatBtn.onclick = toggleChatbot;
    if (sendBtn) sendBtn.onclick = sendMessage;
    
    if (input) {
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') sendMessage();
        });
    }

    // Close on Escape (just hide, don't clear)
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && dropdown.classList.contains('active')) {
            closeChatbot();
        }
    });

    // Add navbar icon
    function addNavbarIcon() {
        if (document.getElementById('itchamps-chatbot-navbar-icon')) return;

        const navbar = document.querySelector('.navbar .navbar-nav');
        if (!navbar) {
            setTimeout(addNavbarIcon, 500);
            return;
        }

        const li = document.createElement('li');
        li.id = 'itchamps-chatbot-navbar-icon';
        li.className = 'nav-item';
        li.style.marginRight = '12px';

        const a = document.createElement('a');
        a.className = 'nav-link';
        a.href = 'javascript:void(0)';
        a.title = 'ITChamps AI Assistant';
        a.onclick = toggleChatbot;
        a.innerHTML = '<span style="font-size: 22px;">🤖</span>';

        li.appendChild(a);
        navbar.insertBefore(li, navbar.firstChild);
        
        console.log('Navbar icon added');
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(addNavbarIcon, 1000);
        });
    } else {
        setTimeout(addNavbarIcon, 1000);
    }

    console.log('ITChamps Chatbot initialized successfully');
})();