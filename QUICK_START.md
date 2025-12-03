# 🚀 Quick Start Guide - GitHub Chatbot Integration

## ⚡ 60-Second Setup

### 1. Install Dependencies (30 seconds)
```bash
cd ~/frappe-bench
source env/bin/activate
pip install requests
```

### 2. Restart Server (30 seconds)
```bash
bench restart
```

### 3. Test It! (Immediately)
Open your Frappe site → Click 🤖 icon → Type: **"Show repo info"**

---

## 📝 What to Ask the Chatbot

### GitHub Commands

| Ask This | Get This |
|----------|----------|
| "Show repo info" | Repository details (stars, forks, language) |
| "Show recent commits" | Last 5 commits with links |
| "Show open issues" | Current open issues |
| "Show closed issues" | Closed issues |
| "Show pull requests" | Open PRs |
| "Show branches" | All repository branches |
| "Show contributors" | Top contributors |

### Employee/HR Commands (Existing Features)

| Ask This | Get This |
|----------|----------|
| "Show my leaves" | Your leave balance |
| "Who is my manager?" | Manager details |
| "Find employees" | Employee search |

---

## 🔧 Optional: Add GitHub Token (Higher Rate Limits)

**Why?** Increase from 60 to 5,000 API requests per hour

### Step 1: Generate Token
Visit: https://github.com/settings/tokens/new

Settings:
- **Note**: "Frappe Chatbot"
- **Scopes**: Check `public_repo`
- Click **Generate token**
- Copy the token (starts with `ghp_`)

### Step 2: Add to Frappe
```bash
cd ~/frappe-bench/sites/your-site-name
nano site_config.json
```

Add this line:
```json
{
  "github_token": "ghp_your_token_here"
}
```

### Step 3: Restart
```bash
bench restart
```

---

## ✅ Verify Installation

### Method 1: Browser Test
1. Open your Frappe site
2. Click the 🤖 chatbot icon
3. Type: "Show repo info"
4. You should see repository details

### Method 2: Python Test
```bash
cd ~/frappe-bench/apps/itchamps
python test_github_integration.py
```

Expected output:
```
✅ Repository: itchamps
✅ Found 5 commits
✅ Found X open issues
✅ Found X branches
✅ Found X contributors
```

---

## 🐛 Troubleshooting

### Error: "App business_theme_v14 is not installed"
**Fixed!** The API endpoint has been updated. Just restart:
```bash
bench restart
```

### Error: "GitHub API Error"
**Solutions:**
1. Check internet connection
2. Verify repo exists: https://github.com/Nusrath02/itchamps
3. Add GitHub token (see above)

### Error: "Module not found"
```bash
bench restart
bench clear-cache
```

### Chatbot doesn't appear
```bash
bench build
bench restart
```

---

## 📁 Files Created

| File | Purpose |
|------|---------|
| [itchamps/api/github_helper.py](itchamps/api/github_helper.py) | GitHub API wrapper |
| [itchamps/api/chatbot.py](itchamps/api/chatbot.py) | Chatbot backend (updated) |
| [itchamps/public/js/chatbot.js](itchamps/public/js/chatbot.js) | Chatbot UI (fixed) |
| [README_GITHUB_SETUP.md](README_GITHUB_SETUP.md) | Detailed setup guide |
| [GITHUB_INTEGRATION_SUMMARY.md](GITHUB_INTEGRATION_SUMMARY.md) | Integration summary |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System architecture |
| [test_github_integration.py](test_github_integration.py) | Test script |
| [QUICK_START.md](QUICK_START.md) | This file |

---

## 🎯 Example Conversation

```
You: Show repo info

Bot: Repository Information:
• Name: itchamps
• Description: ITChamps HR Management with AI Chatbot
• Language: Python
• Stars: ⭐ 0
• Forks: 🍴 0
• Open Issues: 🐛 0
• URL: View on GitHub
• Created: 2025-12-01
• Last Updated: 2025-12-03
```

```
You: Show recent commits

Bot: Recent Commits:
• 1bb58bc by Nusrath02
  chabot ai
  [2025-12-03](link)

• 63cd8b0 by Nusrath02
  chat input
  [2025-12-03](link)

• 4dae926 by Nusrath02
  chatbot css
  [2025-12-02](link)
```

---

## 💡 Pro Tips

1. **Case Insensitive**: "Show Repo Info" = "show repo info" = "SHOW REPO INFO"
2. **Flexible Phrasing**: "Show commits" = "Recent commits" = "Latest commits"
3. **No Token Needed**: Works without GitHub token (with 60 req/hour limit)
4. **Markdown Support**: Bot responses support **bold**, *italic*, links, lists
5. **Error Recovery**: If something fails, check browser console (F12)

---

## 🔗 Quick Links

- **Your Repository**: https://github.com/Nusrath02/itchamps
- **GitHub API Status**: https://www.githubstatus.com/
- **GitHub Tokens**: https://github.com/settings/tokens
- **Check Rate Limit**: https://api.github.com/rate_limit

---

## 📞 Need Help?

1. Read [README_GITHUB_SETUP.md](README_GITHUB_SETUP.md) for detailed instructions
2. Check [ARCHITECTURE.md](ARCHITECTURE.md) to understand how it works
3. Run `python test_github_integration.py` to diagnose issues
4. Check Frappe logs: `bench --site your-site-name logs`
5. Check browser console: Press F12 in browser

---

## 🎉 Success Checklist

- [ ] Installed `requests` library
- [ ] Restarted Frappe server
- [ ] Chatbot icon (🤖) appears in navbar
- [ ] Can open chatbot by clicking icon
- [ ] "Show repo info" returns repository details
- [ ] "Show commits" returns commit history
- [ ] (Optional) Added GitHub token for higher limits

If all checks pass: **✅ You're done!**

---

**Last Updated**: 2025-12-03
**Repository**: https://github.com/Nusrath02/itchamps
**Status**: ✅ Ready to use
