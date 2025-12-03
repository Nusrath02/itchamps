// ITChamps AI Chatbot - Frontend (JavaScript Only)
(function() {
    // Prevent double initialization
    if (window.itchampsChatlbotInitialized) return;
    window.itchampsChatlbotInitialized = true;

    console.log('ITChamps Chatbot initializing...');

    // Load external CSS file
    const cssLink = document.createElement('link');
    cssLink.rel = 'stylesheet';
    cssLink.href = '/assets/itchamps/css/chatbot.css';
    document.head.appendChild(cssLink);

    // Remove any existing chatbot buttons from other apps
    setTimeout(function() {
        const existingBots = document.querySelectorAll('[class*="chatbot"], [id*="chatbot"], .widget-chatbot');
        existingBots.forEach(function(bot) {
            if (!bot.id || !bot.id.includes('itchamps')) {
                bot.style.display = 'none';
            }
        });
    }, 2000);

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