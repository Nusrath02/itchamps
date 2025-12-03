# GitHub API Integration Setup

## Overview
Your chatbot is now integrated with GitHub API to fetch information from your `Nusrath02/itchamps` repository.

## Features
The chatbot can now handle:
- ✅ Repository information (stars, forks, issues)
- ✅ Recent commits
- ✅ Open/closed issues
- ✅ Pull requests
- ✅ Branches
- ✅ Contributors
- ✅ Code search (requires authentication)

## Setup Instructions

### 1. GitHub Personal Access Token (Optional but Recommended)

For higher rate limits and private repository access, add a GitHub token:

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Or visit: https://github.com/settings/tokens

2. Click "Generate new token (classic)"

3. Give it a name like "Frappe Chatbot"

4. Select scopes:
   - `repo` (for private repos)
   - `public_repo` (for public repos only)

5. Generate and copy the token

### 2. Configure in Frappe

**Option A: Add to site_config.json**
```bash
# Navigate to your site directory
cd ~/frappe-bench/sites/your-site-name

# Edit site_config.json
nano site_config.json
```

Add this line:
```json
{
  "github_token": "your_github_token_here"
}
```

**Option B: Use Frappe environment variables**
```bash
# Add to your .env file or environment
export GITHUB_TOKEN="your_github_token_here"
```

### 3. Update API Endpoint in chatbot.js

The JavaScript file needs to point to the correct Frappe API endpoint.

Find this line in `itchamps/public/js/chatbot.js`:
```javascript
method: 'business_theme_v14.business_theme_v14.chatbot_api.get_response',
```

Change it to:
```javascript
method: 'itchamps.api.chatbot.get_response',
```

### 4. Install Python Dependencies

```bash
# Navigate to your frappe-bench
cd ~/frappe-bench

# Activate virtual environment
source env/bin/activate

# Install requests library (if not already installed)
pip install requests
```

### 5. Restart Frappe

```bash
bench restart
```

## Usage Examples

Once setup is complete, you can ask the chatbot:

### Repository Information
- "Show repo info"
- "Tell me about the repository"
- "Repository details"

### Commits
- "Show recent commits"
- "Latest commits"
- "What are the recent commits?"

### Issues
- "Show open issues"
- "Show closed issues"
- "List issues"

### Pull Requests
- "Show pull requests"
- "Show open PRs"
- "Show closed PRs"

### Branches
- "Show branches"
- "List all branches"

### Contributors
- "Show contributors"
- "Who are the contributors?"

## Rate Limits

**Without Token:**
- 60 requests per hour

**With Token:**
- 5,000 requests per hour

## Troubleshooting

### Error: "App business_theme_v14 is not installed"
Update the API endpoint path in chatbot.js as shown in step 3 above.

### Error: "GitHub API Error"
1. Check your internet connection
2. Verify the repository exists: https://github.com/Nusrath02/itchamps
3. Check rate limits: https://api.github.com/rate_limit

### Error: "Module not found"
```bash
cd ~/frappe-bench
bench restart
bench clear-cache
```

## File Structure

```
itchamps/
├── api/
│   ├── chatbot.py          # Main chatbot logic
│   └── github_helper.py    # GitHub API integration
└── public/
    └── js/
        └── chatbot.js      # Frontend chatbot UI
```

## Security Notes

- ⚠️ Never commit your GitHub token to version control
- ⚠️ Add `site_config.json` to `.gitignore`
- ✅ Use environment variables for sensitive data
- ✅ Use tokens with minimal required scopes

## Testing

Test the integration:
```python
# In Frappe console (bench console)
from itchamps.api.github_helper import GitHubHelper

github = GitHubHelper(owner="Nusrath02", repo="itchamps")
info = github.get_repository_info()
print(info)
```

## Support

If you encounter issues:
1. Check Frappe logs: `bench --site your-site-name logs`
2. Check browser console for JavaScript errors
3. Verify API endpoint in chatbot.js matches your app name
