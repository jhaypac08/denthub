# DentHub Public Website

A modern, responsive one-page website for DentHub Dental Clinic.

## Features

- **Hero Section** - Eye-catching introduction with call-to-action buttons
- **Services** - Showcase of dental services offered
- **About Us** - Clinic information and statistics
- **Branches** - Dynamic branch listing from backend API with operating hours
- **Contact Form** - Get in touch form with branch selection
- **Responsive Design** - Works perfectly on mobile, tablet, and desktop

## Running the Website

### Option 1: Using Python HTTP Server (Port 3000)
```powershell
cd c:\xampp\htdocs\Denthub\public-website
python -m http.server 3000
```
Then visit: http://localhost:3000

### Option 2: Using PHP Built-in Server (Port 8080)
```powershell
cd c:\xampp\htdocs\Denthub\public-website
php -S localhost:8080
```
Then visit: http://localhost:8080

### Option 3: Using XAMPP (Port 80)
Simply access: http://localhost/Denthub/public-website/

### Option 4: On Network (Accessible from other devices)
```powershell
python -m http.server 3000 --bind 192.168.1.18
```
Then visit from any device: http://192.168.1.18:3000

## Backend Integration

The website connects to the DentHub backend API at:
- API URL: http://192.168.1.18:8000/api

### Features Connected to Backend:
- Branch listings with operating hours
- Branch selection in contact form
- Real-time branch status (Active/Inactive)

## File Structure

```
public-website/
├── index.html      # Main HTML file
├── styles.css      # All styles and responsive design
├── script.js       # JavaScript for interactivity and API calls
└── README.md       # This file
```

## Technologies Used

- **HTML5** - Semantic markup
- **CSS3** - Modern styling with animations
- **JavaScript** - Vanilla JS for interactivity
- **Font Awesome** - Icons
- **Fetch API** - Backend integration

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers

## Customization

### Colors
Edit the CSS variables in `styles.css`:
```css
:root {
    --primary-color: #00B2A9;
    --secondary-color: #17a2b8;
    --dark-color: #2c3e50;
}
```

### API Endpoint
Edit the API URL in `script.js`:
```javascript
const API_URL = 'http://192.168.1.18:8000/api';
```

## Contact

For questions or support, contact: info@denthub.com
