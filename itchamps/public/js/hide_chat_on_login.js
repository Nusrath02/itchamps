// hide_chat_on_login.js
(function() {
  function hideChatOnLogin() {
    // detect classic desk login which uses hash "#login" OR path "/login"
    var onLogin = window.location.hash && window.location.hash.indexOf('login') !== -1
                  || window.location.pathname.indexOf('/login') !== -1;

    if (!onLogin) return;

    // list of common chatbot widget selectors (covers many widget implementations)
    var selectors = [
      '#chatbot',          // id
      '.chatbot',          // generic class
      '.chat-launcher',
      '.chat-button',
      '.bot-launcher',
      '.floating-chat',
      '.df-chat',          // dialogflow widgets
      '[data-chatbot]',    // data attribute
      '.intercom-launcher', // intercom
      '.tawk-min-container' // tawk.to
    ];

    // attempt to hide or remove all matches
    var q = selectors.join(',');
    var nodes = document.querySelectorAll(q);
    nodes.forEach(function(n){
      try {
        // visually hide first (instant)
        n.style.display = 'none';
        // remove from DOM (if possible)
        if (n.parentNode) n.parentNode.removeChild(n);
      } catch(e){}
    });

    // also try removing any iframe-based widgets
    var iframes = document.querySelectorAll('iframe');
    iframes.forEach(function(f){
      // small heuristic: many chat widgets have iframe src containing "chat", "widget", "tawk"
      var s = f.src || '';
      if (/chat|widget|tawk|intercom|bot|dialogflow/i.test(s)) {
        try { f.style.display = 'none'; if (f.parentNode) f.parentNode.removeChild(f); } catch(e){}
      }
    });
  }

  // run on load, and again shortly after in case widget loads late
  window.addEventListener('load', hideChatOnLogin);
  window.addEventListener('hashchange', hideChatOnLogin);
  setTimeout(hideChatOnLogin, 600);
})();
