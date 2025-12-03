# Logo Files

## Required Logo

Please add your logo file to this directory:

**Filename:** `itchamps_iemp.png`

### Logo Specifications:

- **Format:** PNG (with transparent background recommended)
- **Dimensions:**
  - Height: 28px (will be auto-scaled)
  - Width: Auto (recommended aspect ratio for navbar)
- **File size:** Keep under 100KB for fast loading

### Where it's used:

- Navbar (top navigation bar)
- Login page
- Brand identity across the app

### How to add your logo:

1. Save your logo as `itchamps_iemp.png`
2. Upload it to: `itchamps/public/images/`
3. Clear cache in Frappe
4. Refresh your browser

The logo path is configured in `itchamps/hooks.py` as:
```
app_logo_url = "/assets/itchamps/images/itchamps_iemp.png"
```
