# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "itchamps"
app_title = "ITChamps"
app_publisher = "ITChamps"
app_description = "ITChamps HR Management with AI Chatbot"
app_icon = "octicon octicon-organization"
app_color = "grey"  # Changed from #1e3c72 to use default Frappe theme
app_email = "info@itchamps.com"
app_license = "MIT"


# Website settings
website_context = {
    "brand_html": '<img src="/assets/itchamps/images/itchamps_iemp.png" alt="ITChamps" class="navbar-brand-image">',
    "top_bar_items": [],
}

# App logo
app_logo_url = "/assets/itchamps/images/itchamps_iemp.png"

# Includes in <head>
app_include_css = [
    f"/assets/itchamps/css/itchamps_theme.css?v={app_version}",  # Theme first
    f"/assets/itchamps/css/chatbot.css?v={app_version}",          # Chatbot second
    
]

app_include_js = [
    f"/assets/itchamps/js/chatbot_ui.js?v={app_version}",
    f"/assets/itchamps/js/chatbot.js?v={app_version}",
    f"/assets/itchamps/js/hide_chat_on_login.js?v={app_version}",
   
]

# Make sure our JS and CSS loads on web pages too
web_include_css = [
    f"/assets/itchamps/css/chatbot.css?v={app_version}"
]

web_include_js = [
    f"/assets/itchamps/js/chatbot_ui.js?v={app_version}",
    f"/assets/itchamps/js/chatbot.js?v={app_version}",
    f"/assets/itchamps/js/hide_chat_on_login.js?v={app_version}"
]
