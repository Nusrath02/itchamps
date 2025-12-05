// Main Chatbot Controller (logic only)
// This file acts as the "index.js" or entry point
// It relies on ItChampsChatbotUI (loaded from chatbot_ui.js) for all visual elements

(function () {
    // Prevent double initialization
    if (window.chatbotControllerInitialized) return;
    window.chatbotControllerInitialized = true;

    // Do not show chatbot for Guests or on Login page
    if (frappe.session.user === 'Guest' || window.location.pathname.includes('/login')) {
        return;
    }

    // Check if UI class is loaded
    if (typeof ItChampsChatbotUI === 'undefined') {
        console.error('ItChampsChatbotUI class not found. Make sure chatbot_ui.js is loaded.');
        return;
    }

    // Initialize UI
    const ui = new ItChampsChatbotUI();
    ui.init();
    ui.resetMessages(); // Show initial welcome message

    // logic: Handle sending messages
    ui.onSend(async function (userMsg) {
        if (!userMsg) return;

        // 1. Show user message immediately
        ui.addUserMessage(userMsg);

        // 2. Show loading state
        ui.showLoading();

        try {
            // 3. Call Backend API
            const response = await frappe.call({
                method: 'itchamps.api.chatbot.get_response',
                args: { message: userMsg }
            });

            // 4. Remove loading
            ui.hideLoading();

            // 5. Display Bot Response
            const botMsg = response.message?.message || "Sorry, I couldn't process that.";
            ui.addBotMessage(botMsg);

        } catch (error) {
            ui.hideLoading();
            console.error('Chatbot API Error:', error);

            // Handle specific Frappe error structures if needed
            let errorText = error.message || error.statusText || "Something went wrong.";
            if (error._server_messages) {
                try {
                    const msgs = JSON.parse(error._server_messages);
                    errorText = msgs.join('\n');
                } catch (e) { }
            }

            ui.addErrorMessage(errorText);
        }
    });

    // Add Navbar Icon (optional, if you want it)
    // Passing the toggle function from UI to the navbar helper
    // We defer this slightly to ensure navbar exists
    setTimeout(() => {
        ui.addNavbarIcon(() => ui.toggle());
    }, 1000);

    console.log('Chatbot Controller initialized');
})();