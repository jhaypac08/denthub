# Quick Start Guide - Website Content Management

## Prerequisites
- Backend server running on http://192.168.1.18:8000
- Frontend admin running on http://192.168.1.18:5174
- Public website running on http://192.168.1.18:3000

## Starting the Servers

### 1. Start Backend (Django)
```powershell
cd c:\xampp\htdocs\Denthub\backend
python manage.py runserver 192.168.1.18:8000
```

### 2. Start Frontend Admin (Vue.js)
```powershell
cd c:\xampp\htdocs\Denthub\frontend
npm run dev
```

### 3. Start Public Website
```powershell
cd c:\xampp\htdocs\Denthub\public-website
python -m http.server 3000 --bind 192.168.1.18
```

## Accessing Website Content Management

1. Open browser: http://192.168.1.18:5174
2. Login with your admin credentials
3. Click on sidebar: **Public Website > Website Content**

## Available Tabs

### Hero Section
- **What to edit**: Main landing page title, subtitle, and button texts
- **Example**: Change "Welcome to DentHub Dental Clinic" to your custom message
- **Tip**: Keep it short and impactful

### Services
- **What to edit**: Dental services offered
- **How**: Click "Add Service" or edit existing ones
- **Fields**: Title, Description, Icon, Order, Active status
- **Tip**: Lower order numbers appear first

### About
- **What to edit**: About clinic description, statistics, features
- **Sections**:
  - Description text
  - Patient count, Years in business, Number of dentists
  - Feature bullet points
- **Tip**: Use realistic, verifiable numbers

### Contact
- **What to edit**: Contact section text, social media links, footer
- **Fields**:
  - Section title and subtitle
  - Facebook, Twitter, Instagram, LinkedIn URLs
  - Footer copyright text
- **Tip**: Include full URLs (https://...)

### Site Settings
- **What to edit**: Global site configuration
- **Fields**:
  - Site name (appears in navbar)
  - Patient portal URL
  - Primary and secondary colors
- **Tip**: Use color picker for easy selection

## Making Changes

1. **Edit**: Modify fields in any tab
2. **Save**: Click the save button at bottom of form
3. **Verify**: Visit public site and refresh to see changes

## Example: Changing Hero Title

1. Go to **Hero Section** tab
2. Edit **Title** field: "Welcome to Your Dental Home"
3. Click **Save Hero Section**
4. See success notification
5. Visit http://192.168.1.18:3000 and refresh
6. New title appears!

## Example: Adding a New Service

1. Go to **Services** tab
2. Click **Add Service** button
3. Fill in:
   - Title: "Emergency Dental Care"
   - Description: "24/7 emergency services for urgent dental needs"
   - Icon: Select "fa-user-md"
   - Order: 6
   - Active: Checked
4. Click **Save**
5. Visit public site to see new service card

## Example: Updating Colors

1. Go to **Site Settings** tab
2. Click color picker for **Primary Color**
3. Choose new color (e.g., #FF6B6B)
4. Click **Save Site Settings**
5. Refresh public site - buttons and accents change color!

## Troubleshooting

### Content not updating on public site?
- Hard refresh: Ctrl + Shift + R (or Cmd + Shift + R on Mac)
- Check browser console for errors
- Verify API endpoint: http://192.168.1.18:8000/api/website/hero/

### Save button not working?
- Check backend server is running
- Look for errors in browser console (F12)
- Verify you're logged in

### Services not appearing?
- Make sure "Active" is checked
- Check "Order" field is set
- Verify service was saved successfully

## Testing API Endpoints

### PowerShell
```powershell
# Test hero section
Invoke-WebRequest -Uri "http://192.168.1.18:8000/api/website/hero/" | Select-Object -ExpandProperty Content

# Test services
Invoke-WebRequest -Uri "http://192.168.1.18:8000/api/website/services/" | Select-Object -ExpandProperty Content
```

### Browser
Simply visit in browser:
- http://192.168.1.18:8000/api/website/hero/
- http://192.168.1.18:8000/api/website/services/
- http://192.168.1.18:8000/api/website/about/
- http://192.168.1.18:8000/api/website/contact/
- http://192.168.1.18:8000/api/website/settings/

## Best Practices

1. **Save Often**: Don't make too many changes before saving
2. **Preview**: Always check public site after changes
3. **Backup**: Consider taking database backups before major edits
4. **Testing**: Test on different devices/browsers
5. **Consistency**: Maintain consistent tone across all sections

## Important Notes

- Changes are **immediate** - no approval workflow
- Only **active** content appears on public site
- **Service order** determines display sequence
- **Colors** must be valid hex codes (#RRGGBB)
- **Social links** are optional - leave blank if not used

## Support

For issues or questions:
1. Check documentation: WEBSITE_CONTENT_MANAGEMENT.md
2. Review implementation: WEBSITE_CONTENT_IMPLEMENTATION.md
3. Check browser console for errors
4. Verify all servers are running

---

**Happy Editing! 🎉**
