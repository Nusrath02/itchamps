/**
 * ChatbotUI Class
 * Handles all visual elements, DOM manipulation, and Markdown rendering.
 * Separated from the main logic for cleaner code structure.
 */

window.ItChampsChatbotUI = class ItChampsChatbotUI {
    constructor(options = {}) {
        this.options = options;
        this.elements = {};
        this.initialized = false;
    }

    init() {
        if (this.initialized) return;
        this.renderInterface();
        this.cacheElements();
        this.bindEvents();
        this.initialized = true;
        console.log('Chatbot UI initialized');
    }

    /**
     * Renders the main chatbot HTML into the document body
     */
    renderInterface() {
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

        const container = document.createElement('div');
        container.innerHTML = chatbotHTML;
        document.body.appendChild(container);
    }

    /**
     * Cache DOM elements for easy access
     */
    cacheElements() {
        this.elements = {
            dropdown: document.getElementById('chatbotDropdown'),
            overlay: document.getElementById('chatbotOverlay'),
            closeBtn: document.getElementById('chatbotCloseBtn'),
            floatBtn: document.getElementById('chatbotFloatBtn'),
            input: document.getElementById('chatbotInput'),
            sendBtn: document.getElementById('chatbotSendBtn'),
            messages: document.getElementById('chatbotMessages')
        };
    }

    /**
     * Bind click and keypress events
     */
    bindEvents() {
        const { closeBtn, overlay, floatBtn, sendBtn, input, dropdown } = this.elements;

        // UI toggling events
        if (closeBtn) closeBtn.onclick = () => this.closeAndClear();
        if (overlay) overlay.onclick = () => this.close();
        if (floatBtn) floatBtn.onclick = () => this.toggle();

        // Escape key to close
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && dropdown.classList.contains('active')) {
                this.close();
            }
        });

        // Input events are handled by the main controller (chatbot.js) using callbacks
        // We will expose a method to register the send callback
    }

    onSend(callback) {
        const { sendBtn, input } = this.elements;
        if (sendBtn) {
            sendBtn.onclick = () => {
                const text = input.value.trim();
                if (text) callback(text);
            };
        }
        if (input) {
            input.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    const text = input.value.trim();
                    if (text) callback(text);
                }
            });
        }
    }

    /**
     * UI Actions
     */
    toggle() {
        if (this.elements.dropdown.classList.contains('active')) {
            this.close();
        } else {
            this.open();
        }
    }

    open() {
        this.elements.dropdown.classList.add('active');
        this.elements.overlay.classList.add('active');
        setTimeout(() => this.elements.input && this.elements.input.focus(), 100);
    }

    close() {
        this.elements.dropdown.classList.remove('active');
        this.elements.overlay.classList.remove('active');
    }

    closeAndClear() {
        this.close();
        this.resetMessages();
    }

    clearInput() {
        if (this.elements.input) this.elements.input.value = '';
    }

    scrollToBottom() {
        if (this.elements.messages) {
            this.elements.messages.scrollTop = this.elements.messages.scrollHeight;
        }
    }

    /**
     * Message Rendering
     */
    addUserMessage(text) {
        const escapedMsg = this.escapeHtml(text);
        this.appendMessageHTML(`
            <div class="chat-msg user">
                <div class="msg-bubble">${escapedMsg}</div>
            </div>
        `);
        this.clearInput();
        this.scrollToBottom();
    }

    addBotMessage(text) {
        const formattedMsg = this.parseMarkdown(text);
        this.appendMessageHTML(`
            <div class="chat-msg bot">
                <div class="msg-bubble">${formattedMsg}</div>
            </div>
        `);
        this.scrollToBottom();
    }

    addErrorMessage(text) {
        const escapedMsg = this.escapeHtml(text);
        this.appendMessageHTML(`
            <div class="chat-msg bot">
                <div class="msg-bubble" style="color: #e53e3e; border-color: #feb2b2;">
                    ⚠️ <strong>Error:</strong> ${escapedMsg}
                </div>
            </div>
        `);
        this.scrollToBottom();
    }

    showLoading() {
        this.appendMessageHTML(`
            <div class="chat-msg bot" id="chatbotLoading">
                <div class="msg-bubble">
                    <div class="typing-indicator">
                        <span></span><span></span><span></span>
                    </div>
                </div>
            </div>
        `);
        this.scrollToBottom();
    }

    hideLoading() {
        const loading = document.getElementById('chatbotLoading');
        if (loading) loading.remove();
    }

    resetMessages() {
        if (!this.elements.messages) return;

        const introMessages = [
            "👋 Hi! I'm your AI assistant. How can I help you today?",
            "**I can help you with:**\n\n1. Leave balance & applications\n2. GitHub repository info\n3. Employee search\n4. Profile & Manager info"
        ];

        this.elements.messages.innerHTML = introMessages.map((text) => `
            <div class="chat-msg bot">
                <div class="msg-bubble">${this.parseMarkdown(text)}</div>
            </div>
        `).join('');
    }

    appendMessageHTML(html) {
        if (this.elements.messages) {
            this.elements.messages.innerHTML += html;
        }
    }

    /**
     * Utilities
     */
    escapeHtml(text) {
        if (!text) return '';
        return text.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');
    }

    parseMarkdown(text) {
        if (!text) return '';

        let t = this.escapeHtml(text);

        // Basic Markdown Rules
        t = t.replace(/^### (.*$)/gim, '<h3>$1</h3>')
            .replace(/^## (.*$)/gim, '<h2>$1</h2>')
            .replace(/^# (.*$)/gim, '<h1>$1</h1>')
            .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
            .replace(/^\* (.+)$/gim, '<li>$1</li>')
            .replace(/^- (.+)$/gim, '<li>$1</li>')
            .replace(/```([^`]+)```/g, '<pre><code>$1</code></pre>')
            .replace(/`([^`]+)`/g, '<code>$1</code>')
            .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank">$1</a>')
            .replace(/\n\n/g, '</p><p>');

        // Wrap lists (simple heuristic)
        if (t.includes('<li>')) {
            t = t.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');
        }

        return `<p>${t}</p>`.replace(/<p><\/p>/g, '');
    }

    // Navbar Icon
    addNavbarIcon(callback) {
        if (document.getElementById('chatbot-navbar-icon')) return;

        const navbar = document.querySelector('.navbar .navbar-nav');
        if (!navbar) {
            // If navbar isn't ready, try again shortly
            setTimeout(() => this.addNavbarIcon(callback), 500);
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
        a.onclick = callback; // Bind toggle function
        a.innerHTML = '<span style="font-size: 22px;">🤖</span>';

        li.appendChild(a);
        navbar.insertBefore(li, navbar.firstChild);
    }
};
