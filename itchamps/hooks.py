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

# Dynamic versioning for cache busting
app_version = str(int(time.time()))  # current timestamp, changes every deploy

# duplicate removed


# Website settings
website_context = {
    "brand_html": '<img src="/assets/itchamps/images/itchamps_iemp.png" alt="ITChamps" class="navbar-brand-image">',
    "top_bar_items": [],
}

# App logo
app_logo_url = "/assets/itchamps/images/itchamps_iemp.png"

# Includes in <head>
app_include_css = [
    # f"/assets/itchamps/css/itchamps_theme.css?v={app_version}",
    f"/assets/itchamps/css/chatbot.css?v={app_version}"
]

app_include_js = [
    f"/assets/itchamps/js/chatbot_ui.js?v={app_version}",
    f"/assets/itchamps/js/chatbot.js?v={app_version}"
]

# itchamps/hooks.py
app_include_js = "/assets/itchamps/js/hide_chat_on_login.js"
web_include_js = "/assets/itchamps/js/hide_chat_on_login.js"


# Make sure our JS loads after page is ready
web_include_css = [
    f"/assets/itchamps/css/chatbot.css?v={app_version}"
]

web_include_js = [
    f"/assets/itchamps/js/chatbot_ui.js?v={app_version}",
    f"/assets/itchamps/js/chatbot.js?v={app_version}"
]
