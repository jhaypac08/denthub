# Website Content Management

This feature allows you to manage all the content on the public-facing DentHub website from the admin panel.

## Features

### 1. Hero Section Management
- Edit main title and subtitle
- Customize call-to-action buttons (text and links)
- Enable/disable sections

### 2. Services Management
- Add, edit, and delete services
- Choose from predefined Font Awesome icons
- Set display order
- Enable/disable individual services
- Full CRUD operations

### 3. About Section Management
- Edit about text and description
- Manage statistics (Patients, Years, Dentists)
- Add/remove feature highlights
- Enable/disable section

### 4. Contact Information
- Update contact section titles
- Manage social media links (Facebook, Twitter, Instagram, LinkedIn)
- Edit footer text
- Enable/disable section

### 5. Site Settings
- Change site name
- Update patient portal URL
- Customize primary and secondary colors
- Real-time color preview

## Access

Navigate to **Public Website > Website Content** in the admin panel sidebar.

## API Endpoints

All endpoints support public read access (GET) and authenticated write access (POST/PUT/DELETE):

- `/api/website/hero/` - Hero section content
- `/api/website/services/` - Services list
- `/api/website/about/` - About section with features
- `/api/website/contact/` - Contact information
- `/api/website/settings/` - Site settings

## Database Models

### HeroSection
- title, subtitle
- primary_button_text, primary_button_link
- secondary_button_text, secondary_button_link
- is_active

### Service
- title, description
- icon (Font Awesome class)
- order (for sorting)
- is_active

### AboutSection
- title, description
- patients_count, patients_label
- years_count, years_label
- dentists_count, dentists_label
- is_active

### AboutFeature
- about_section (ForeignKey)
- text
- order

### ContactInfo
- section_title, section_subtitle
- facebook_url, twitter_url, instagram_url, linkedin_url
- footer_text
- is_active

### SiteSettings
- site_name
- patient_portal_url
- primary_color, secondary_color

## Initial Data

Run this command to populate initial website content:

```bash
python manage.py populate_website_content
```

This creates default content matching the current public website design.

## How It Works

1. **Backend**: Django models store all content in the database
2. **Admin Panel**: Vue.js interface provides easy content editing
3. **Public Website**: JavaScript fetches content via API on page load
4. **Real-time Updates**: Changes in admin panel immediately reflect on public site after page refresh

## Usage Tips

1. **Hero Section**: Keep titles concise and impactful
2. **Services**: Use descriptive icons that match the service type
3. **About Stats**: Use numbers that are realistic and verifiable
4. **Colors**: Use hex color codes (#RRGGBB format)
5. **Social Links**: Provide full URLs including https://

## Technical Notes

- All endpoints support CORS for public access
- Images/icons use Font Awesome 6.4.0
- Color changes update CSS custom properties dynamically
- Service order determines display sequence (lowest first)
- Only active sections/services appear on public website
