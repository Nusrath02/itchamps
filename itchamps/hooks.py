# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "itchamps"
app_title = "ITChamps"
app_publisher = "ITChamps"
app_description = "ITChamps HR Management with AI Chatbot"
app_icon = "octicon octicon-organization"
app_color = "#1e3c72"
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
    "/assets/itchamps/css/itchamps_theme.css"
]

app_include_js = [
    "/assets/itchamps/js/chatbot.js"
]

# Make sure our JS loads after page is ready
web_include_css = [
    "/assets/itchamps/css/itchamps_theme.css"
]

web_include_js = [
    "/assets/itchamps/js/chatbot.js"
]
