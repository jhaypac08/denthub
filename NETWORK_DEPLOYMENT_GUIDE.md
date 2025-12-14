# DentHub Local Network Deployment Guide

## Your Network Configuration
- **WiFi IP Address:** 192.168.1.18
- **Backend URL:** http://192.168.1.18:8000
- **Frontend URL:** http://192.168.1.18:5173

---

## Quick Start for Beta Testing

### Step 1: Start MySQL (XAMPP)
1. Open XAMPP Control Panel
2. Start MySQL service

### Step 2: Start Backend Server
- Double-click: `start_backend_network.bat`
- Backend will run on: http://192.168.1.18:8000

### Step 3: Start Frontend Server
- Double-click: `start_frontend_network.bat`
- Frontend will run on: http://192.168.1.18:5173

### Step 4: Share with Beta Testers
Share this URL with anyone on your WiFi network:
```
http://192.168.1.18:5173
```

---

## For Beta Testers

### Requirements
- Must be connected to the same WiFi network
- Any modern web browser (Chrome, Firefox, Edge)

### Access Instructions
1. Open your browser
2. Go to: `http://192.168.1.18:5173`
3. Login with provided credentials

### Test Accounts
- **Admin:** (Create admin account)
- **Staff:** (Create staff account)
- **Patient:** Use Patient ID as username, last name as password

---

## Troubleshooting

### Can't Access from Other Devices?

1. **Check Firewall:**
   - Ports 5173 and 8000 should be allowed
   - Run `start_backend_network.bat` and `start_frontend_network.bat` as Administrator if needed

2. **Verify IP Address:**
   - Run: `ipconfig` in Command Prompt
   - Look for "Wireless LAN adapter Wi-Fi" -> "IPv4 Address"
   - Update all config files if IP changed

3. **Check Network:**
   - All testers must be on the same WiFi
   - Corporate networks might block local connections

4. **Restart Services:**
   - Stop both servers (Ctrl+C in command windows)
   - Restart using the .bat files

### Backend Not Starting?

- Ensure MySQL is running in XAMPP
- Check if port 8000 is already in use
- Verify virtual environment is activated

### Frontend Not Starting?

- Check if port 5173 is available
- Try: `cd frontend` then `npm install`
- Restart the frontend server

---

## Advanced Configuration

### If Your IP Address Changes
If your WiFi IP changes, update these files:

1. **backend/denthub_project/settings.py:**
   - Update CSRF_TRUSTED_ORIGINS

2. **frontend/.env:**
   - Update VITE_API_BASE_URL

3. **frontend/vite.config.js:**
   - Update proxy target

4. **frontend/src/services/api.js:**
   - Update API_BASE_URL

### Production Deployment (Future)
For actual production deployment:
- Set DEBUG = False in settings.py
- Use proper database (PostgreSQL)
- Configure proper ALLOWED_HOSTS
- Use HTTPS with SSL certificates
- Deploy on cloud server (AWS, DigitalOcean, etc.)

---

## Security Notes for Beta Testing

⚠️ **Important:**
- This setup is for LOCAL NETWORK testing only
- NOT secure for internet deployment
- Use test data only, not real patient information
- Change all passwords after testing

---

## Testing Checklist

### Features to Test:
- [ ] Login/Logout functionality
- [ ] Patient registration
- [ ] Appointment scheduling
- [ ] Treatment records
- [ ] Photo upload
- [ ] Message system
- [ ] Password change (first login)
- [ ] Mobile responsiveness
- [ ] Different user roles (Admin, Staff, Patient)

### Report Issues:
Note any bugs, crashes, or unexpected behavior for fixes.

---

## Stop Servers

To stop servers:
1. Go to the command window running the server
2. Press `Ctrl + C`
3. Type `Y` to confirm
4. Repeat for both frontend and backend

---

## Support

If issues persist:
1. Check browser console (F12) for errors
2. Check backend terminal for error messages
3. Ensure MySQL database is running
4. Verify all services are on the same network

---

**Last Updated:** December 7, 2025
**Network IP:** 192.168.1.18
