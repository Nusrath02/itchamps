# ITChamps Chatbot Troubleshooting Guide

## Chatbot Not Appearing After Deployment

If the chatbot is not showing up after deploying to Frappe Cloud, follow these steps:

### 1. **Clear Browser Cache**
The chatbot files (JS/CSS) might be cached. Clear your browser cache or do a hard refresh:
- **Windows/Linux:** `Ctrl + Shift + R` or `Ctrl + F5`
- **Mac:** `Cmd + Shift + R`

### 2. **Clear Frappe Cache** (Most Important!)
On your Frappe site, you need to clear the server cache:

**Option A: Via UI**
1. Click the search bar (or press `Ctrl + K`)
2. Type: **"Clear Cache"**
3. Click on "Clear Cache" command
4. Refresh the page

**Option B: Via Frappe Cloud Console**
Go to your site's console and run:
```bash
bench --site [your-site-name] clear-cache
bench --site [your-site-name] clear-website-cache
```

### 3. **Verify App Installation**
1. Go to your Frappe site
2. Click the search bar (`Ctrl + K`)
3. Type: **"Installed Applications"**
4. Check that **ITChamps** appears in the list with version **aa3bcff**

### 4. **Check Assets are Built**
After clearing cache, check if the chatbot assets are loading:

1. Open browser Developer Tools (`F12`)
2. Go to the **Console** tab
3. Look for the message: `ITChamps Chatbot initialized successfully`
4. Go to the **Network** tab and refresh
5. Look for these files:
   - `/assets/itchamps/js/chatbot.js` (should return 200 OK)
   - `/assets/itchamps/css/itchamps_theme.css` (should return 200 OK)

### 5. **Check for JavaScript Errors**
1. Open browser Developer Tools (`F12`)
2. Go to **Console** tab
3. Look for any red error messages
4. If you see errors related to `frappe.call`, the API might not be working

### 6. **Test the Chatbot API Directly**
Open browser console (`F12`) and test the API:

```javascript
frappe.call({
    method: 'itchamps.api.chatbot.get_response',
    args: { message: 'hello' },
    callback: function(r) {
        console.log(r);
    }
});
```

If this works, you should see a response with `success: true`.

### 7. **Look for the Chatbot Elements**
The chatbot should show:
- A **floating button** (🤖) in the bottom-right corner
- A **navbar icon** (🤖) in the top navigation bar

If these don't appear, the JavaScript might not be loading.

### 8. **Rebuild Assets** (If needed)
If assets still don't load, you may need to rebuild:

Via Frappe Cloud Console:
```bash
bench --site [your-site-name] build
```

Or trigger a rebuild by clicking "Update Available" button in Frappe Cloud dashboard.

### 9. **Check Permissions**
Make sure you're logged in as a user with proper permissions. The chatbot requires:
- Access to Employee doctype
- Access to Leave Application doctype
- Access to Leave Allocation doctype

### 10. **Common Issues**

**Issue:** Chatbot button appears but clicking does nothing
- **Solution:** Check browser console for JavaScript errors

**Issue:** Chatbot appears but API returns errors
- **Solution:** Check if you have Employee records and proper user permissions

**Issue:** Theme is not applied
- **Solution:** Clear cache and hard refresh browser

**Issue:** "Frappe is not defined" error
- **Solution:** The chatbot.js is loading before Frappe. Clear cache and rebuild.

## Quick Fix Checklist

✅ Clear Frappe cache via UI (`Ctrl + K` → "Clear Cache")
✅ Hard refresh browser (`Ctrl + Shift + R`)
✅ Check browser console for errors (`F12`)
✅ Verify app is installed ("Installed Applications")
✅ Check network tab for asset loading
✅ Look for floating 🤖 button (bottom-right)
✅ Look for navbar 🤖 icon (top navigation)

## Still Not Working?

If the chatbot still doesn't appear:

1. **Check the build logs** in Frappe Cloud for any errors during deployment
2. **Verify file structure** - Make sure all files are in the correct locations
3. **Check Frappe version** - This app is built for Frappe v15
4. **Contact support** with browser console errors and network tab screenshots

## Expected Behavior

When working correctly:
- ✅ Floating chatbot button (🤖) appears in bottom-right corner
- ✅ Chatbot icon in navbar
- ✅ Blue gradient theme applied to the interface
- ✅ Console shows: "ITChamps Chatbot initialized successfully"
- ✅ Clicking button opens chat interface
- ✅ Can send messages and receive responses

## File Locations to Verify

```
itchamps/
├── api/
│   └── chatbot.py          # Backend API
├── public/
│   ├── js/
│   │   └── chatbot.js      # Frontend JavaScript
│   └── css/
│       └── itchamps_theme.css  # Theme styles
└── hooks.py                # App configuration
```

## Support

For more help, check:
- GitHub Issues: https://github.com/Nusrath02/itchamps/issues
- Frappe Forum: https://discuss.frappe.io/
