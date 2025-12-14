// API Base URL
const API_URL = 'http://192.168.1.18:8000/api';

// Hero Carousel
let currentSlideIndex = 0;
let carouselInterval;
let carouselIntervalDuration = 5000; // Default 5 seconds

function showSlide(index) {
    const slides = document.querySelectorAll('.hero-slide');
    const indicators = document.querySelectorAll('.indicator');
    
    if (index >= slides.length) {
        currentSlideIndex = 0;
    } else if (index < 0) {
        currentSlideIndex = slides.length - 1;
    } else {
        currentSlideIndex = index;
    }
    
    slides.forEach(slide => slide.classList.remove('active'));
    indicators.forEach(indicator => indicator.classList.remove('active'));
    
    slides[currentSlideIndex].classList.add('active');
    indicators[currentSlideIndex].classList.add('active');
}

function moveSlide(direction) {
    showSlide(currentSlideIndex + direction);
    resetCarouselInterval();
}

function currentSlide(index) {
    showSlide(index);
    resetCarouselInterval();
}

function autoSlide() {
    currentSlideIndex++;
    showSlide(currentSlideIndex);
}

function startCarousel() {
    carouselInterval = setInterval(autoSlide, carouselIntervalDuration);
}

function resetCarouselInterval() {
    clearInterval(carouselInterval);
    startCarousel();
}

// Add swipe functionality to carousel
function addSwipeToCarousel(carousel) {
    let startX = 0;
    let endX = 0;
    let startY = 0;
    let endY = 0;
    let isDragging = false;
    
    // Touch events for mobile/tablet
    carousel.addEventListener('touchstart', (e) => {
        startX = e.changedTouches[0].screenX;
        startY = e.changedTouches[0].screenY;
    }, { passive: true });
    
    carousel.addEventListener('touchend', (e) => {
        endX = e.changedTouches[0].screenX;
        endY = e.changedTouches[0].screenY;
        handleSwipe();
    }, { passive: true });
    
    // Mouse events for desktop
    carousel.addEventListener('mousedown', (e) => {
        isDragging = true;
        startX = e.screenX;
        startY = e.screenY;
        carousel.style.cursor = 'grabbing';
    });
    
    carousel.addEventListener('mousemove', (e) => {
        if (!isDragging) return;
        e.preventDefault();
    });
    
    carousel.addEventListener('mouseup', (e) => {
        if (!isDragging) return;
        isDragging = false;
        endX = e.screenX;
        endY = e.screenY;
        carousel.style.cursor = 'grab';
        handleSwipe();
    });
    
    carousel.addEventListener('mouseleave', () => {
        if (isDragging) {
            isDragging = false;
            carousel.style.cursor = 'grab';
        }
    });
    
    // Set cursor style
    carousel.style.cursor = 'grab';
    
    function handleSwipe() {
        const swipeThreshold = 50; // Minimum distance for swipe
        const diffX = startX - endX;
        const diffY = Math.abs(startY - endY);
        
        // Only trigger if horizontal swipe is larger than vertical (not scrolling)
        if (Math.abs(diffX) > swipeThreshold && Math.abs(diffX) > diffY) {
            if (diffX > 0) {
                // Swiped left - show next slide
                moveSlide(1);
            } else {
                // Swiped right - show previous slide
                moveSlide(-1);
            }
        }
    }
}

// Fetch and render dynamic content
async function loadWebsiteContent() {
    // Load settings first to get carousel interval
    await loadSiteSettings();
    
    // Then load other content in parallel
    await Promise.all([
        loadHeroSection(),
        loadServices(),
        loadAboutSection(),
        loadContactInfo()
    ]);
}

// Load Hero Section
async function loadHeroSection() {
    try {
        const response = await fetch(`${API_URL}/website/hero/`);
        const heroSlides = await response.json();
        
        // Filter active slides and sort by order
        const activeSlides = heroSlides.filter(h => h.is_active).sort((a, b) => a.order - b.order);
        
        if (activeSlides.length > 0) {
            const heroCarousel = document.querySelector('.hero-carousel');
            if (heroCarousel) {
                // Generate slides HTML
                const slidesHTML = activeSlides.map(hero => {
                    const hasBackground = hero.background_image ? 'has-background' : '';
                    const backgroundStyle = hero.background_image ? `style="background-image: url('${hero.background_image}');"` : '';
                    const heroIcon = hero.icon || 'fa-tooth';
                    
                    return `
                        <div class="hero-slide ${hasBackground}" ${backgroundStyle}>
                            <div class="container">
                                <div class="hero-content">
                                    <h1 class="hero-title">${hero.title}</h1>
                                    <p class="hero-subtitle">${hero.subtitle}</p>
                                    <div class="hero-buttons">
                                        <a href="${hero.primary_button_link}" class="btn btn-primary">
                                            <i class="fas fa-calendar-check"></i> ${hero.primary_button_text}
                                        </a>
                                        <a href="${hero.secondary_button_link}" class="btn btn-secondary">
                                            <i class="fas fa-info-circle"></i> ${hero.secondary_button_text}
                                        </a>
                                    </div>
                                </div>
                                ${!hero.background_image ? `<div class="hero-image"><i class="fas ${heroIcon}"></i></div>` : ''}
                            </div>
                        </div>
                    `;
                }).join('');
                
                // Generate indicators HTML
                const indicatorsHTML = activeSlides.map((_, index) => 
                    `<span class="indicator" onclick="currentSlide(${index})"></span>`
                ).join('');
                
                // Update carousel content
                heroCarousel.innerHTML = `
                    ${slidesHTML}
                    <div class="carousel-indicators">
                        ${indicatorsHTML}
                    </div>
                `;
                
                // Initialize carousel
                showSlide(0);
                startCarousel(); // Start carousel with loaded interval
                
                // Add swipe functionality
                addSwipeToCarousel(heroCarousel);
            }
        }
    } catch (error) {
        console.error('Error loading hero section:', error);
    }
}

// Load Services
async function loadServices() {
    try {
        const response = await fetch(`${API_URL}/website/services/`);
        const services = await response.json();
        
        const servicesGrid = document.querySelector('.services-grid');
        if (servicesGrid && services.length > 0) {
            servicesGrid.innerHTML = services.map(service => `
                <div class="service-card">
                    <div class="service-icon">
                        <i class="fas ${service.icon}"></i>
                    </div>
                    <h3>${service.title}</h3>
                    <p>${service.description}</p>
                </div>
            `).join('');
        }
    } catch (error) {
        console.error('Error loading services:', error);
    }
}

// Load About Section
async function loadAboutSection() {
    try {
        const response = await fetch(`${API_URL}/website/about/`);
        const data = await response.json();
        const about = data.find(a => a.is_active) || data[0];
        
        if (about) {
            const aboutText = document.querySelector('.about-text');
            if (aboutText) {
                aboutText.querySelector('h2').textContent = about.title;
                aboutText.querySelector('p').textContent = about.description;
                
                // Update features
                const featuresContainer = aboutText.querySelector('.features');
                if (featuresContainer && about.features) {
                    featuresContainer.innerHTML = about.features.map(feature => `
                        <div class="feature">
                            <i class="fas fa-check-circle"></i>
                            <span>${feature.text}</span>
                        </div>
                    `).join('');
                }
            }
            
            // Update stats
            const statCards = document.querySelectorAll('.stat-card');
            if (statCards.length >= 3) {
                statCards[0].querySelector('h3').textContent = about.patients_count;
                statCards[0].querySelector('p').textContent = about.patients_label;
                
                statCards[1].querySelector('h3').textContent = about.years_count;
                statCards[1].querySelector('p').textContent = about.years_label;
                
                statCards[2].querySelector('h3').textContent = about.dentists_count;
                statCards[2].querySelector('p').textContent = about.dentists_label;
            }
        }
    } catch (error) {
        console.error('Error loading about section:', error);
    }
}

// Load Contact Info
async function loadContactInfo() {
    try {
        const response = await fetch(`${API_URL}/website/contact/`);
        const data = await response.json();
        const contact = data.find(c => c.is_active) || data[0];
        
        if (contact) {
            const contactSection = document.querySelector('.contact');
            if (contactSection) {
                contactSection.querySelector('.section-title').textContent = contact.section_title;
                contactSection.querySelector('.section-subtitle').textContent = contact.section_subtitle;
            }
            
            // Update footer
            const footerText = document.querySelector('.footer-bottom p');
            if (footerText) {
                footerText.textContent = contact.footer_text;
            }
            
            // Update social links
            const socialLinks = document.querySelector('.social-links');
            if (socialLinks) {
                let socialHTML = '';
                if (contact.facebook_url) socialHTML += `<a href="${contact.facebook_url}" target="_blank"><i class="fab fa-facebook"></i></a>`;
                if (contact.twitter_url) socialHTML += `<a href="${contact.twitter_url}" target="_blank"><i class="fab fa-twitter"></i></a>`;
                if (contact.instagram_url) socialHTML += `<a href="${contact.instagram_url}" target="_blank"><i class="fab fa-instagram"></i></a>`;
                if (contact.linkedin_url) socialHTML += `<a href="${contact.linkedin_url}" target="_blank"><i class="fab fa-linkedin"></i></a>`;
                socialLinks.innerHTML = socialHTML;
            }
        }
    } catch (error) {
        console.error('Error loading contact info:', error);
    }
}

// Load Site Settings
async function loadSiteSettings() {
    try {
        const response = await fetch(`${API_URL}/website/settings/`);
        const data = await response.json();
        const settings = data[0];
        
        if (settings) {
            // Update site name
            const navBrand = document.querySelector('.nav-brand span');
            if (navBrand) {
                navBrand.textContent = settings.site_name;
            }
            
            // Update patient portal link
            const portalLink = document.getElementById('patient-portal-link');
            if (portalLink) {
                portalLink.href = settings.patient_portal_url;
            }
            
            // Update CSS variables for colors
            document.documentElement.style.setProperty('--primary-color', settings.primary_color);
            document.documentElement.style.setProperty('--secondary-color', settings.secondary_color);
            
            // Update carousel interval
            if (settings.carousel_interval) {
                carouselIntervalDuration = settings.carousel_interval;
                // Restart carousel with new interval if already running
                if (carouselInterval) {
                    resetCarouselInterval();
                }
            }
        }
    } catch (error) {
        console.error('Error loading site settings:', error);
    }
}

// Mobile menu toggle
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');

if (hamburger) {
    hamburger.addEventListener('click', () => {
        navMenu.classList.toggle('active');
    });
}

// Close mobile menu when clicking on a link
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
        navMenu.classList.remove('active');
    });
});

// Smooth scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Navbar scroll effect
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.boxShadow = '0 5px 20px rgba(0, 0, 0, 0.1)';
    } else {
        navbar.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
    }
});

// Active nav link on scroll
const sections = document.querySelectorAll('section[id]');

window.addEventListener('scroll', () => {
    let current = '';
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if (scrollY >= sectionTop - 200) {
            current = section.getAttribute('id');
        }
    });

    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${current}`) {
            link.classList.add('active');
        }
    });
});

// Fetch branches from backend
async function fetchBranches() {
    const branchesList = document.getElementById('branches-list');
    
    try {
        const response = await fetch(`${API_URL}/branches/`);
        const branches = await response.json();
        
        if (branches.length === 0) {
            branchesList.innerHTML = '<p class="loading">No branches available at the moment.</p>';
            return;
        }

        branchesList.innerHTML = branches.filter(branch => branch.is_active).map(branch => {
            // Format operating hours
            const hours = formatOperatingHours(branch);
            
            return `
                <div class="branch-card">
                    <h3>${branch.name}</h3>
                    <span class="branch-status ${branch.is_active ? 'active' : 'inactive'}">
                        ${branch.is_active ? 'Active' : 'Inactive'}
                    </span>
                    
                    <div class="branch-info">
                        <i class="fas fa-map-marker-alt"></i>
                        <span>${branch.address}</span>
                    </div>
                    
                    <div class="branch-info">
                        <i class="fas fa-phone"></i>
                        <span>${branch.phone}</span>
                    </div>
                    
                    <div class="branch-info">
                        <i class="fas fa-envelope"></i>
                        <span>${branch.email}</span>
                    </div>
                    
                    ${branch.manager ? `
                        <div class="branch-info">
                            <i class="fas fa-user-tie"></i>
                            <span>Manager: ${branch.manager}</span>
                        </div>
                    ` : ''}
                    
                    <div class="branch-hours">
                        <h4><i class="fas fa-clock"></i> Operating Hours</h4>
                        ${hours}
                    </div>
                </div>
            `;
        }).join('');

        // Populate branch options in contact form
        const branchSelect = document.getElementById('branch');
        branchSelect.innerHTML = '<option value="">Select a branch</option>' +
            branches.filter(b => b.is_active).map(b => 
                `<option value="${b.id}">${b.name}</option>`
            ).join('');

    } catch (error) {
        console.error('Error fetching branches:', error);
        branchesList.innerHTML = '<p class="loading">Unable to load branches. Please try again later.</p>';
    }
}

// Format operating hours for display
function formatOperatingHours(branch) {
    const days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];
    const scheduleMap = new Map();
    
    // Group days with same schedule
    days.forEach(day => {
        const open = branch[`${day}_open`];
        const close = branch[`${day}_close`];
        const closed = branch[`${day}_closed`];
        
        const key = `${open}|${close}|${closed}`;
        
        if (!scheduleMap.has(key)) {
            scheduleMap.set(key, {
                open: open || '',
                close: close || '',
                closed: closed || false,
                days: []
            });
        }
        
        scheduleMap.get(key).days.push(day);
    });
    
    // Convert to array and format
    const schedules = Array.from(scheduleMap.values()).map(schedule => {
        const daysList = schedule.days;
        const formattedDays = [];
        let rangeStart = null;
        
        for (let i = 0; i < daysList.length; i++) {
            const currentDayIndex = days.indexOf(daysList[i]);
            const nextDayIndex = i < daysList.length - 1 ? days.indexOf(daysList[i + 1]) : -1;
            
            if (rangeStart === null) {
                rangeStart = currentDayIndex;
            }
            
            if (nextDayIndex !== currentDayIndex + 1) {
                if (rangeStart === currentDayIndex) {
                    formattedDays.push(capitalizeDay(days[currentDayIndex]));
                } else {
                    formattedDays.push(`${capitalizeDay(days[rangeStart])} - ${capitalizeDay(days[currentDayIndex])}`);
                }
                rangeStart = null;
            }
        }
        
        return {
            days: formattedDays.join(', '),
            time: schedule.closed ? 'Closed' : `${formatTime12Hour(schedule.open)} - ${formatTime12Hour(schedule.close)}`,
            closed: schedule.closed
        };
    });
    
    return schedules.map(s => `
        <div class="hours-item">
            <span class="day">${s.days}:</span>
            <span class="time ${s.closed ? 'text-muted' : ''}">${s.time}</span>
        </div>
    `).join('');
}

// Helper function to capitalize day
function capitalizeDay(day) {
    return day.charAt(0).toUpperCase() + day.slice(1);
}

// Helper function to format time to 12-hour
function formatTime12Hour(time) {
    if (!time) return 'N/A';
    
    const [hours, minutes] = time.split(':');
    let hour = parseInt(hours);
    const ampm = hour >= 12 ? 'PM' : 'AM';
    
    hour = hour % 12 || 12;
    
    return `${hour}:${minutes} ${ampm}`;
}

// Contact form submission
const contactForm = document.getElementById('contactForm');
if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = {
            name: document.getElementById('name').value,
            email: document.getElementById('email').value,
            phone: document.getElementById('phone').value,
            branch: document.getElementById('branch').value,
            message: document.getElementById('message').value
        };
        
        // Here you would typically send this to your backend
        console.log('Form submitted:', formData);
        
        // Show success message
        alert('Thank you for contacting us! We will get back to you soon.');
        contactForm.reset();
    });
}

// Load branches when page loads
document.addEventListener('DOMContentLoaded', () => {
    loadWebsiteContent();
    fetchBranches();
});

// Intersection Observer for fade-in animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe all service cards and branch cards
setTimeout(() => {
    document.querySelectorAll('.service-card, .branch-card, .stat-card').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'all 0.6s ease';
        observer.observe(el);
    });
}, 500);

// Initialize carousel on page load
document.addEventListener('DOMContentLoaded', () => {
    showSlide(0);
    // Carousel will start after settings are loaded in loadWebsiteContent
    
    // Pause carousel on hover
    const carousel = document.querySelector('.hero-carousel');
    if (carousel) {
        carousel.addEventListener('mouseenter', () => {
            clearInterval(carouselInterval);
        });
        carousel.addEventListener('mouseleave', () => {
            startCarousel();
        });
    }
});
