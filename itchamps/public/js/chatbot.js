// Initialize chatbot on page load
(function() {
    // Prevent double initialization
    if (window.chatbotInitialized) return;
    window.chatbotInitialized = true;

    console.log('Initializing chatbot...');

    // Simple markdown parser
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
        
        // Lists
        text = text.replace(/^\* (.+)$/gim, '<li>$1</li>');
        text = text.replace(/^- (.+)$/gim, '<li>$1</li>');
        text = text.replace(/^\d+\. (.+)$/gim, '<li>$1</li>');
        
        // Wrap lists
        text = text.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');
        
        // Code blocks
        text = text.replace(/```([^`]+)```/g, '<pre><code>$1</code></pre>');
        
        // Inline code
        text = text.replace(/`([^`]+)`/g, '<code>$1</code>');
        
        // Links
        text = text.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank">$1</a>');
        
        // Line breaks
        text = text.replace(/\n\n/g, '</p><p>');
        text = '<p>' + text + '</p>';
        
        // Clean up empty paragraphs
        text = text.replace(/<p><\/p>/g, '');
        text = text.replace(/<p>(<h[123]>)/g, '$1');
        text = text.replace(/(<\/h[123]>)<\/p>/g, '$1');
        text = text.replace(/<p>(<ul>)/g, '$1');
        text = text.replace(/(<\/ul>)<\/p>/g, '$1');
        
        return text;
    }

    // Create chatbot HTML
    const chatbotHTML = `
        <div class="chatbot-overlay" id="chatbotOverlay"></div>
        
        <div class="chatbot-dropdown" id="chatbotDropdown">
            <div class="chatbot-header">
                <div class="chatbot-header-title">
                    <span>🤖</span>
                    <span>AI Assistant</span>
                </div>
                <button class="chatbot-close-btn" id="chatbotCloseBtn" title="Close">×</button>
            </div>
            <div class="chatbot-messages" id="chatbotMessages">
                <div class="chat-msg bot">
                    <div class="msg-bubble">👋 Hi! I'm your AI assistant. How can I help you today?</div>
                </div>
            </div>
            <div class="chatbot-input-area">
                <input type="text" id="chatbotInput" placeholder="Ask me anything..." />
                <button id="chatbotSendBtn">Send</button>
            </div>
        </div>
        
        <div class="chatbot-float-btn" id="chatbotFloatBtn" title="Open AI Chatbot">
            🤖
        </div>
    `;

    const div = document.createElement('div');
    div.innerHTML = chatbotHTML;
    document.body.appendChild(div);

    // Get elements
    const dropdown = document.getElementById('chatbotDropdown');
    const overlay = document.getElementById('chatbotOverlay');
    const closeBtn = document.getElementById('chatbotCloseBtn');
    const floatBtn = document.getElementById('chatbotFloatBtn');
    const input = document.getElementById('chatbotInput');
    const sendBtn = document.getElementById('chatbotSendBtn');
    const messages = document.getElementById('chatbotMessages');

    function renderInitialMessages() {
        if (!messages) return;
        const introMessages = [
            "👋 Hi! I'm your AI assistant. How can I help you today?",
            `**Rule-based (Weak but Simple)**\n\n- Pattern matching: "show my leaves" → fetch leave records\n- Dies on anything complex\n- Brittle, requires constant maintenance\n\n**Specific tasks** the chatbot MUST handle:\n\n1. "Show my pending leave applications"\n2. "How many sick leaves do I have left?"\n3. "What's my reporting manager's email?"\n4. "Create a new leave request for next Monday"\n5. "Find employees in the Marketing department"`
        ];

        messages.innerHTML = introMessages.map((text) => `
            <div class="chat-msg bot">
                <div class="msg-bubble">${parseMarkdown(text)}</div>
            </div>
        `).join('');
    }

    renderInitialMessages();

    // Send message function
    window.sendMessage = async function() {
        const userMsg = input.value.trim();
        if (!userMsg) return;

        console.log('Sending message:', userMsg);

        // Escape HTML for user message
        const escapedMsg = userMsg.replace(/&/g, '&amp;')
                                  .replace(/</g, '&lt;')
                                  .replace(/>/g, '&gt;');

        // Add user message
        messages.innerHTML += `
            <div class="chat-msg user">
                <div class="msg-bubble">${escapedMsg}</div>
            </div>
        `;
        input.value = '';

        // Add loading indicator
        messages.innerHTML += `
            <div class="chat-msg bot" id="chatbotLoading">
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

            const loading = document.getElementById('chatbotLoading');
            if (loading) loading.remove();

            const botMsg = response.message?.message || "Sorry, I couldn't process that.";
            const formattedMsg = parseMarkdown(botMsg);
            
            messages.innerHTML += `
                <div class="chat-msg bot">
                    <div class="msg-bubble">${formattedMsg}</div>
                </div>
            `;
        } catch (error) {
            const loading = document.getElementById('chatbotLoading');
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

    // Toggle chatbot
    window.toggleChatbot = function() {
        if (dropdown.classList.contains('active')) {
            closeChatbot();
        } else {
            openChatbot();
        }
    };

    // Open chatbot
    window.openChatbot = function() {
        dropdown.classList.add('active');
        overlay.classList.add('active');
        setTimeout(() => input && input.focus(), 100);
        console.log('Chatbot opened');
    };

    // Close chatbot (just hide, don't clear)
    window.closeChatbot = function() {
        dropdown.classList.remove('active');
        overlay.classList.remove('active');
        console.log('Chatbot closed');
    };

    // Close and clear chatbot (only for X button)
    window.closeChatbotAndClear = function() {
        dropdown.classList.remove('active');
        overlay.classList.remove('active');
        
        // Clear chat messages and restore welcome & guidance message
        renderInitialMessages();
        
        console.log('Chatbot closed and cleared');
    };

    // Event listeners
    if (closeBtn) closeBtn.onclick = closeChatbotAndClear;  // X button clears chat
    if (overlay) overlay.onclick = closeChatbot;  // Overlay click just hides
    if (floatBtn) floatBtn.onclick = toggleChatbot;
    if (sendBtn) sendBtn.onclick = sendMessage;
    
    if (input) {
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') sendMessage();
        });
    }

    // Close on Escape
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && dropdown.classList.contains('active')) {
            closeChatbot();
        }
    });

    // Add navbar icon
    function addNavbarIcon() {
        if (document.getElementById('chatbot-navbar-icon')) return;

        const navbar = document.querySelector('.navbar .navbar-nav');
        if (!navbar) {
            setTimeout(addNavbarIcon, 500);
            return;
        }

        const li = document.createElement('li');
        li.id = 'chatbot-navbar-icon';
        li.className = 'nav-item';
        li.style.marginRight = '12px';

        const a = document.createElement('a');
        a.className = 'nav-link';
        a.href = 'javascript:void(0)';
        a.title = 'AI Assistant';
        a.onclick = toggleChatbot;
        a.innerHTML = '<span style="font-size: 22px;">🤖</span>';

        li.appendChild(a);
        navbar.insertBefore(li, navbar.firstChild);
        
        console.log('Navbar icon added');
    }

    // Initialize navbar
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(addNavbarIcon, 1000);
        });
    } else {
        setTimeout(addNavbarIcon, 1000);
    }

    console.log('Chatbot initialized successfully');
})();