# ITChamps - AI-Powered HR Chatbot for ERPNext

AI-powered HR chatbot with role-based access control for Frappe/ERPNext.

## 🎯 What It Does

ITChamps is a chatbot that helps employees get instant answers to HR questions:

- **Check leave balance** - "my leaves", "leave balance"
- **View manager info** - "my manager", "who is my manager"
- **Search employees** - "search employee", "find employee in HR" (Admin/HR/Manager only)
- **View profile** - "my profile", "my info"
- **AI conversations** - Ask anything in natural language

## 🏗️ How It Works

**2-Tier System:**

1. **Rule-Based (Fast & Free)**
   - Detects keywords like "leave", "manager", "profile"
   - Queries ERPNext database directly
   - Returns instant responses

2. **AI-Powered (Smart)**
   - Uses Claude AI for complex questions
   - Understands natural language
   - Provides conversational responses
   - Requires API key (optional)

## 🔐 Security & Access Control

**Role-Based Permissions:**

| Feature              | Admin | HR Manager | HR User | Manager | Employer | Employee |
| -------------------- | ----- | ---------- | ------- | ------- | -------- | -------- |
| Search All Employees | ✅     | ✅          | ✅       | ✅       | ❌        | ❌        |
| View Own Data        | ✅     | ✅          | ✅       | ✅       | ✅        | ✅        |

**Security enforced at application level** - not just UI hiding.

## 📁 Project Structure

```
itchamps/
├── api/
│   ├── chatbot.py          # Main backend endpoint
│   ├── llm_service.py      # Claude AI integration
│   ├── nlu.py              # Intent detection
│   ├── auth_service.py     # User permissions
│   └── constants.py        # Role definitions
│
├── public/
│   ├── css/
│   │   └── chatbot.css     # Chatbot styling
│   └── js/
│       ├── chatbot_ui.js   # UI rendering
│       ├── chatbot.js      # Main controller
│       └── hide_chat_on_login.js
│
└── hooks.py                # Frappe app configuration
```

## 🚀 Installation

### 1. Install Dependencies

```bash
cd frappe-bench
bench get-app https://github.com/Nusrath02/itchamps.git
bench --site your-site install-app itchamps
```

### 2. Configure API Key (Optional - for AI features)

```bash
bench --site your-site set-config anthropic_api_key "sk-ant-your-key-here"
```

### 3. Build and Restart

```bash
bench build --app itchamps
bench restart
```

## 🛠️ Technology Stack

- **Backend:** Python, Frappe Framework
- **Frontend:** JavaScript (Vanilla), CSS
- **AI:** Claude 3 Haiku (Anthropic)
- **Database:** ERPNext HR Module

## 📊 Dependencies

```txt
requests>=2.31.0      # GitHub API integration
anthropic>=0.18.0     # Claude AI (optional)
```

## 🎨 Features

### For All Employees
- ✅ Check own leave balance
- ✅ View leave history
- ✅ See reporting manager
- ✅ View own profile

### For Admin/HR/Manager
- ✅ Search all employees
- ✅ View employee details
- ✅ Filter by department

### AI Features (with API key)
- ✅ Natural language understanding
- ✅ Conversational responses
- ✅ Context-aware answers

## 🔧 Configuration

### Frappe Cloud Deployment

1. Push to GitHub
2. Connect repository in Frappe Cloud
3. Add API key in Config (optional)
4. Deploy

### Local Development

```bash
# Clear cache after changes
bench clear-cache
bench build --app itchamps
bench restart
```

## 📝 Usage Examples

**Check Leaves:**
```
User: "my leaves"
Bot: Shows leave balance by type
```

**Find Manager:**
```
User: "who is my manager"
Bot: Shows manager name, designation, email
```

**Search Employee (Admin/HR/Manager only):**
```
User: "search employee in HR"
Bot: Lists all HR department employees
```

**AI Query (with API key):**
```
User: "How many vacation days do I have left?"
Bot: Intelligent response with leave details
```

## 🐛 Troubleshooting

### Chatbot Not Appearing
1. Clear browser cache (Ctrl + Shift + R)
2. Check `hooks.py` - ensure JS files are loaded
3. Run: `bench build --app itchamps`

### Backend Errors
1. Check error logs: `bench logs`
2. Verify employee is linked to user
3. Ensure dependencies installed

### AI Not Working
1. Verify API key is configured
2. Check you have API credits
3. Model: `claude-3-haiku-20240307` (free tier)

## 📞 Support

- **Repository:** https://github.com/Nusrath02/itchamps
- **Issues:** Report bugs on GitHub
- **Frappe Docs:** https://frappeframework.com/docs

## 📄 License

MIT License

## 🎯 Quick Commands

```bash
# Install
bench get-app https://github.com/Nusrath02/itchamps.git
bench --site site-name install-app itchamps

# Update
cd apps/itchamps
git pull
cd ../..
bench build --app itchamps
bench restart

# Uninstall
bench --site site-name uninstall-app itchamps
```

---

**Version:** 1.0.0  
**Status:** ✅ Production Ready  
**Last Updated:** December 2024
