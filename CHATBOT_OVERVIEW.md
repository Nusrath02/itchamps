# ITChamps AI Chatbot - Complete System Overview

## 📋 Table of Contents
1. [System Architecture](#system-architecture)
2. [How It Works - Step by Step](#how-it-works---step-by-step)
3. [File Connections](#file-connections)
4. [User Interaction Flow](#user-interaction-flow)
5. [Data Flow Diagram](#data-flow-diagram)

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FRAPPE/ERPNEXT SYSTEM                    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐         ┌──────────────┐                 │
│  │   hooks.py   │────────▶│  Asset Loader│                 │
│  │ (Bootstrap)  │         │              │                 │
│  └──────────────┘         └──────┬───────┘                 │
│                                   │                          │
│                    ┌──────────────┼──────────────┐          │
│                    │              │              │          │
│            ┌───────▼────┐  ┌─────▼──────┐  ┌───▼──────┐   │
│            │ theme.css  │  │chatbot.css │  │chatbot.js│   │
│            │  (Global)  │  │  (Styles)  │  │   (UI)   │   │
│            └────────────┘  └────────────┘  └─────┬────┘   │
│                                                    │         │
│                                         ┌──────────▼─────┐  │
│                                         │   User clicks  │  │
│                                         │  chatbot icon  │  │
│                                         └──────────┬─────┘  │
│                                                    │         │
│                                         ┌──────────▼─────┐  │
│                                         │  Frappe.call() │  │
│                                         │   (AJAX/RPC)   │  │
│                                         └──────────┬─────┘  │
│                                                    │         │
│                                         ┌──────────▼─────┐  │
│                                         │  chatbot.py    │  │
│                                         │   (Backend)    │  │
│                                         └──────────┬─────┘  │
│                                                    │         │
│                                    ┌───────────────┼────────┐
│                                    │               │        │
│                            ┌───────▼───┐    ┌─────▼──────┐ │
│                            │ Database  │    │  GitHub    │ │
│                            │ (Queries) │    │    API     │ │
│                            └───────────┘    └────────────┘ │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 How It Works - Step by Step

### **Phase 1: System Initialization (When Frappe Starts)**

#### Step 1: Frappe Reads Configuration
**File: `itchamps/hooks.py`**
```
When Frappe starts → Reads hooks.py → Finds asset includes
```

**What happens:**
- Frappe framework boots up
- Scans all installed apps
- Reads `hooks.py` from each app
- Registers CSS and JS files to be loaded

**Code in hooks.py:**
```python
app_include_css = [
    "/assets/itchamps/css/itchamps_theme.css",  # Global theme
    "/assets/itchamps/css/chatbot.css"           # Chatbot styles
]

app_include_js = [
    "/assets/itchamps/js/chatbot.js"             # Chatbot logic
]
```

---

#### Step 2: Assets Are Loaded into Browser
**Files: All CSS and JS files**

When user opens any page:
```
Browser ← HTML with <link> and <script> tags ← Frappe Server
```

**What gets loaded:**
1. **itchamps_theme.css** - Makes the entire Frappe interface look beautiful
2. **chatbot.css** - Styles specifically for the chatbot modal
3. **chatbot.js** - JavaScript code that creates and controls the chatbot

---

#### Step 3: Chatbot Initializes
**File: `public/js/chatbot.js`**

```javascript
(function() {
    // Prevents running twice
    if (window.chatbotInitialized) return;
    window.chatbotInitialized = true;

    // Creates HTML elements
    // Injects them into the page
    // Sets up event listeners
})();
```

**What happens:**
1. Checks if already initialized (prevents duplicates)
2. Creates all HTML elements:
   - Floating button (🤖 in bottom-right)
   - Overlay (dark background)
   - Chat window (centered modal)
   - Navbar icon
3. Injects these into `document.body`
4. Attaches click handlers, keyboard listeners

**Result:** You see the 🤖 button in bottom-right corner!

---

### **Phase 2: User Interaction**

#### Step 4: User Clicks Chatbot Icon
**File: `public/js/chatbot.js`**

```javascript
floatBtn.onclick = toggleChatbot;
// or
navbarIcon.onclick = toggleChatbot;
```

**What happens:**
1. User clicks 🤖 button (or navbar icon)
2. `toggleChatbot()` function runs
3. Adds `.active` class to:
   - `.chatbot-dropdown` (makes chat visible)
   - `.chatbot-overlay` (shows dark background)
4. Chat window slides down from top-center

**Result:** Chat modal appears on screen!

---

#### Step 5: User Types a Message
**File: `public/js/chatbot.js`**

```
User types "Show my leaves" → Presses Enter or clicks Send
```

**What happens:**
1. `sendMessage()` function is called
2. Message is added to chat display (right-aligned, blue bubble)
3. Input field is cleared
4. Loading indicator appears (three bouncing dots)

---

#### Step 6: JavaScript Calls Backend
**File: `public/js/chatbot.js`**

```javascript
const response = await frappe.call({
    method: 'itchamps.api.chatbot.get_response',
    args: { message: userMsg }
});
```

**What happens:**
1. `frappe.call()` makes an HTTP request to the server
2. Endpoint: `/api/method/itchamps.api.chatbot.get_response`
3. Sends: `{"message": "Show my leaves"}`
4. Waits for response...

---

### **Phase 3: Backend Processing**

#### Step 7: Backend Receives Request
**File: `api/chatbot.py`**

```python
@frappe.whitelist()
def get_response(message):
    """Main chatbot endpoint"""
    message = message.lower().strip()

    # Route to appropriate handler
    if "leave" in message and "pending" in message:
        return handle_pending_leaves()
    # ... more routing logic
```

**What happens:**
1. Frappe routes request to `get_response()` function
2. Gets current user from `frappe.session.user`
3. Converts message to lowercase
4. Analyzes keywords to determine intent
5. Calls appropriate handler function

---

#### Step 8: Backend Queries Database
**File: `api/chatbot.py`**

Example for "Show my leaves":
```python
def handle_pending_leaves():
    # Get employee linked to current user
    employee = get_employee_id()

    # Query database
    pending_leaves = frappe.get_all(
        "Leave Application",
        filters={
            "employee": employee,
            "status": ["in", ["Open", "Pending"]]
        },
        fields=["name", "leave_type", "from_date", "to_date"]
    )

    # Format response
    response = format_leave_data(pending_leaves)
    return {"message": response}
```

**What happens:**
1. Finds employee record linked to logged-in user
2. Queries `Leave Application` DocType in database
3. Filters by employee ID and status
4. Gets relevant fields
5. Formats data as markdown text
6. Returns JSON: `{"message": "**Your Pending Leaves:**\n\n..."}`

---

#### Step 9: Backend Sends Response
**File: `api/chatbot.py`**

```
Backend → JSON Response → Frappe HTTP Layer → Browser
```

Response format:
```json
{
    "message": "**Your Pending Leaves:**\n\n1. Sick Leave: 2024-12-10 to 2024-12-12 (3 days)\n2. Casual Leave: 2024-12-20 to 2024-12-21 (2 days)"
}
```

---

### **Phase 4: Displaying Response**

#### Step 10: Frontend Receives Response
**File: `public/js/chatbot.js`**

```javascript
const botMsg = response.message?.message || "Sorry, I couldn't process that.";
const formattedMsg = parseMarkdown(botMsg);

messages.innerHTML += `
    <div class="chat-msg bot">
        <div class="msg-bubble">${formattedMsg}</div>
    </div>
`;
```

**What happens:**
1. Receives JSON from server
2. Extracts message text
3. Parses markdown to HTML:
   - `**text**` → `<strong>text</strong>`
   - `\n\n` → `</p><p>`
   - Lists, links, code blocks, etc.
4. Creates new chat bubble (left-aligned, white)
5. Adds to chat window
6. Auto-scrolls to bottom
7. Removes loading indicator

**Result:** User sees formatted response in chat!

---

## 📁 File Connections

### **1. hooks.py** (The Bootstrap)
**Location:** `itchamps/hooks.py`

**Purpose:** Tells Frappe what to load

**Connects to:**
- `public/css/itchamps_theme.css` ✅
- `public/css/chatbot.css` ✅
- `public/js/chatbot.js` ✅

**How:** Frappe reads this file and injects CSS/JS into every page

---

### **2. chatbot.css** (The Styling)
**Location:** `itchamps/public/css/chatbot.css`

**Purpose:** Makes chatbot look beautiful

**Styles:**
- `.chatbot-dropdown` - Main chat window (centered, 680x600px)
- `.chatbot-header` - Blue gradient header
- `.chatbot-messages` - Message display area
- `.chat-msg.user` - User messages (blue bubbles, right-aligned)
- `.chat-msg.bot` - Bot messages (white bubbles, left-aligned)
- `.chatbot-float-btn` - Floating 🤖 button
- `.chatbot-overlay` - Dark transparent background
- `.typing-indicator` - Loading animation

**Connected to:** All chatbot HTML elements created by `chatbot.js`

---

### **3. chatbot.js** (The Frontend Brain)
**Location:** `itchamps/public/js/chatbot.js`

**Purpose:** Creates UI and handles user interactions

**Key Functions:**

1. **Initialization:**
   ```javascript
   (function() {
       // Creates HTML
       // Injects into page
       // Sets up events
   })();
   ```

2. **parseMarkdown(text):**
   ```javascript
   // Converts markdown to HTML
   "**bold**" → "<strong>bold</strong>"
   ```

3. **sendMessage():**
   ```javascript
   // Sends user message to backend
   // Displays loading indicator
   // Receives and displays response
   ```

4. **toggleChatbot():**
   ```javascript
   // Shows/hides chat window
   ```

5. **renderInitialMessages():**
   ```javascript
   // Shows welcome message on open
   ```

**Connects to:**
- `chatbot.css` - Uses CSS classes for styling
- `api/chatbot.py` - Calls `get_response()` endpoint
- Frappe framework - Uses `frappe.call()` for API requests

---

### **4. chatbot.py** (The Backend Brain)
**Location:** `itchamps/api/chatbot.py`

**Purpose:** Processes messages and queries database

**Key Functions:**

1. **get_response(message):**
   ```python
   @frappe.whitelist()  # Makes it accessible via HTTP
   def get_response(message):
       # Main entry point
       # Routes to specific handlers
   ```

2. **get_employee_id():**
   ```python
   # Finds employee record for current user
   # Checks: user_id, prefered_email, company_email, personal_email
   ```

3. **handle_pending_leaves():**
   ```python
   # Queries Leave Application DocType
   # Returns formatted list of pending leaves
   ```

4. **handle_leave_balance():**
   ```python
   # Queries Leave Allocation DocType
   # Returns available leave balance by type
   ```

5. **handle_manager_info():**
   ```python
   # Finds reporting manager
   # Returns manager details
   ```

6. **handle_employee_search():**
   ```python
   # Searches employees by department
   ```

7. **handle_github_query():**
   ```python
   # Integrates with GitHub API
   # Returns repo info, commits, issues, etc.
   ```

**Connects to:**
- Frappe Database (via `frappe.get_all()`, `frappe.get_doc()`)
- GitHub API (via `github_helper.py`)
- Frontend JavaScript (via HTTP/JSON)

---

### **5. debug_employee.py** (Testing Tool)
**Location:** `itchamps/debug_employee.py`

**Purpose:** Debug and test employee configuration

**Functions:**

1. **debug_employee_config():**
   - Checks if employee is linked to user
   - Lists leave allocations
   - Lists leave applications
   - Shows reporting manager

2. **fix_employee_link(employee_name):**
   - Links employee to current user

3. **test_chatbot_response(message):**
   - Tests chatbot without using UI
   - Directly calls backend function

**Usage:**
```bash
bench console
>>> from itchamps.debug_employee import debug_employee_config
>>> debug_employee_config()
```

**Connects to:**
- `api/chatbot.py` - Calls `get_response()` for testing
- Frappe database - Queries employee records

---

### **6. itchamps_theme.css** (Global Styling)
**Location:** `itchamps/public/css/itchamps_theme.css`

**Purpose:** Styles the entire Frappe/ERPNext interface

**Styles:**
- Navbar (blue-teal gradient)
- Sidebar (white text)
- Buttons (rounded, gradient)
- Forms (improved styling)
- Cards (shadows, borders)

**Does NOT style the chatbot** - That's in `chatbot.css`

**Connected to:** All pages in Frappe system

---

## 👤 User Interaction Flow

### Complete Journey: From Click to Response

```
┌─────────────────────────────────────────────────────────────┐
│ 1. USER ACTION                                              │
│    User clicks 🤖 button                                    │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│ 2. UI OPENS                                                 │
│    chatbot.js → toggleChatbot()                             │
│    → Adds .active class                                     │
│    → Chat window slides down                                │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│ 3. USER TYPES                                               │
│    "Show my leaves" → Presses Enter                         │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│ 4. FRONTEND PROCESSING                                      │
│    chatbot.js → sendMessage()                               │
│    → Displays user message (blue bubble)                    │
│    → Shows loading indicator (3 dots)                       │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│ 5. API CALL                                                 │
│    frappe.call({                                            │
│        method: 'itchamps.api.chatbot.get_response',         │
│        args: { message: "Show my leaves" }                  │
│    })                                                       │
│                                                             │
│    HTTP POST → /api/method/itchamps.api.chatbot.get_response│
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│ 6. BACKEND RECEIVES                                         │
│    chatbot.py → @frappe.whitelist()                         │
│    → get_response(message)                                  │
│    → message = "show my leaves"                             │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│ 7. INTENT DETECTION                                         │
│    if "leave" in message:                                   │
│        if "pending" in message:                             │
│            → handle_pending_leaves()                        │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│ 8. GET EMPLOYEE                                             │
│    get_employee_id()                                        │
│    → Queries: Employee DocType                              │
│    → Filters: user_id = frappe.session.user                 │
│    → Returns: "HR-EMP-00001"                                │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│ 9. QUERY DATABASE                                           │
│    frappe.get_all("Leave Application", {                    │
│        "employee": "HR-EMP-00001",                          │
│        "status": ["in", ["Open", "Pending"]]                │
│    })                                                       │
│    → Returns: [{name: "LA-0001", ...}, ...]                 │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│ 10. FORMAT RESPONSE                                         │
│     Format as markdown:                                     │
│     "**Your Pending Leaves:**\n\n                          │
│      1. Sick Leave: 2024-12-10 to 2024-12-12\n             │
│      2. Casual Leave: 2024-12-20 to 2024-12-21"            │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│ 11. SEND RESPONSE                                           │
│     return {"message": markdown_text}                       │
│     → HTTP Response (JSON)                                  │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│ 12. FRONTEND RECEIVES                                       │
│     response = await frappe.call(...)                       │
│     → response.message.message = "**Your Pending..."        │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│ 13. PARSE MARKDOWN                                          │
│     parseMarkdown(text)                                     │
│     → "**text**" becomes "<strong>text</strong>"            │
│     → "\n\n" becomes "</p><p>"                             │
│     → Returns HTML                                          │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│ 14. DISPLAY RESPONSE                                        │
│     messages.innerHTML += `                                 │
│         <div class="chat-msg bot">                          │
│             <div class="msg-bubble">${html}</div>           │
│         </div>                                              │
│     `                                                       │
│     → Remove loading indicator                              │
│     → Scroll to bottom                                      │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│ 15. USER SEES RESULT                                        │
│     Bot message appears (white bubble, left side)           │
│     Formatted with bold headers, lists, etc.                │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Data Flow Diagram

### How Data Moves Through the System

```
USER INPUT                    FRONTEND                  BACKEND                 DATABASE
    │                            │                         │                       │
    │  1. "Show my leaves"       │                         │                       │
    ├───────────────────────────>│                         │                       │
    │                            │                         │                       │
    │                            │  2. frappe.call()       │                       │
    │                            ├────────────────────────>│                       │
    │                            │    POST /api/method     │                       │
    │                            │    {message: "..."}     │                       │
    │                            │                         │                       │
    │                            │                         │  3. Query Employee   │
    │                            │                         ├─────────────────────>│
    │                            │                         │    WHERE user_id=?   │
    │                            │                         │                       │
    │                            │                         │  4. Employee ID      │
    │                            │                         │<─────────────────────┤
    │                            │                         │    "HR-EMP-00001"    │
    │                            │                         │                       │
    │                            │                         │  5. Query Leaves     │
    │                            │                         ├─────────────────────>│
    │                            │                         │    WHERE employee=?  │
    │                            │                         │    AND status=?      │
    │                            │                         │                       │
    │                            │                         │  6. Leave Records    │
    │                            │                         │<─────────────────────┤
    │                            │                         │    [{...}, {...}]    │
    │                            │                         │                       │
    │                            │  7. JSON Response       │                       │
    │                            │<────────────────────────┤                       │
    │                            │    {message: "**Your.."}│                       │
    │                            │                         │                       │
    │  8. Display formatted      │                         │                       │
    │<───────────────────────────┤                         │                       │
    │     "Your Pending Leaves:" │                         │                       │
    │     1. Sick Leave...       │                         │                       │
    │                            │                         │                       │
```

---

## 🔍 Deep Dive: Key Technologies

### Frappe Framework
- **What it is:** Python web framework (like Django/Flask but for ERPNext)
- **What it provides:**
  - Database ORM (`frappe.get_all()`, `frappe.get_doc()`)
  - User authentication (`frappe.session.user`)
  - HTTP routing (`@frappe.whitelist()`)
  - Asset management (CSS/JS bundling)
  - DocType system (tables in database)

### frappe.call() - The Bridge
**What it does:** Makes AJAX requests from frontend to backend

**Frontend:**
```javascript
frappe.call({
    method: 'itchamps.api.chatbot.get_response',
    args: { message: "Hello" }
}).then(response => {
    console.log(response.message);
});
```

**Backend:**
```python
@frappe.whitelist()  # Makes function accessible via HTTP
def get_response(message):
    return {"message": "Hi there!"}
```

**Behind the scenes:**
```
JavaScript                     HTTP                      Python
frappe.call()  ──────────────> POST /api/method  ────────> @frappe.whitelist()
               <──────────────  JSON Response    <────────  return {...}
```

---

## 🚀 Summary: The Complete Flow

### In Simple Terms:

1. **Startup:**
   - Frappe reads `hooks.py`
   - Loads CSS and JS files
   - JavaScript creates chatbot UI

2. **User Interaction:**
   - User clicks chatbot button
   - Types a message
   - Presses Send

3. **Frontend Processing:**
   - JavaScript captures message
   - Calls backend API using `frappe.call()`

4. **Backend Processing:**
   - Python receives message
   - Determines what user wants
   - Queries database for relevant data
   - Formats response as markdown

5. **Response Display:**
   - JavaScript receives response
   - Converts markdown to HTML
   - Displays in chat window
   - User sees formatted answer

### Key Connections:

```
hooks.py ────> Loads all files
chatbot.js ───> Creates UI, handles clicks, calls API
chatbot.py ───> Processes requests, queries database
chatbot.css ──> Makes everything look beautiful
```

---

## 🎯 What Makes It Work?

1. **Frappe Framework** - Provides the foundation
2. **hooks.py** - Tells Frappe what to load
3. **chatbot.js** - Creates UI and handles user interactions
4. **chatbot.py** - Processes messages and queries data
5. **chatbot.css** - Makes it visually appealing
6. **Database** - Stores all employee and leave data

Everything is connected through Frappe's framework, which handles:
- User authentication
- Database queries
- HTTP routing
- Asset loading
- Session management

---

**This is a living document. As the chatbot evolves, update this overview to reflect new features and connections.**
