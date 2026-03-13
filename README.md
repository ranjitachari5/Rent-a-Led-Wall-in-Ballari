# 📸 Crazy Vision - Professional Photography Services Website

A modern, responsive website for photographer services built with Flask. Features service listings, booking system, photo gallery, reviews, and admin dashboard.

## ✨ Features

- **🎯 Service Showcase**: Display 6 photography services with detailed descriptions and pricing
- **📅 Booking System**: Easy-to-use booking form with location mapping via Leaflet
- **💳 Payment Integration**: Ready for Razorpay and Stripe integration
- **🖼️ Photo Gallery**: Beautiful filterable gallery to showcase work
- **⭐ Reviews & Testimonials**: Client reviews with rating system
- **📊 Admin Dashboard**: Complete booking and review management
- **🌓 Dark/Light Theme**: Toggle between dark and light modes
- **📱 Responsive Design**: Works perfectly on desktop, tablet, and mobile

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone or download the project**
```bash
cd "Rent a Led Wall in Ballari"
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python app.py
```

5. **Open in browser**
```
http://localhost:5000
```

## 📁 Project Structure

```
Rent a Led Wall in Ballari/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── database.db           # SQLite database (auto-created)
├── static/
│   ├── css/
│   │   ├── base.css          # Base styles (nav, buttons, utilities)
│   │   ├── index.css         # Homepage styles
│   │   ├── services.css      # Services page styles
│   │   ├── booking.css       # Booking form styles
│   │   ├── gallery.css       # Gallery styles
│   │   ├── testimonials.css  # Reviews section styles
│   │   ├── admin.css         # Admin dashboard styles
│   │   └── success.css       # Success page styles
│   └── gallery/          # Photo gallery images (placeholder)
└── templates/
    ├── base.html             # Base template with nav/footer
    ├── index.html            # Homepage
    ├── services.html         # All services listing
    ├── service-detail.html   # Service details page
    ├── gallery.html          # Photo gallery
    ├── booking.html          # Booking form
    ├── payment.html          # Payment page
    ├── reviews.html          # Reviews and testimonials
    ├── success.html          # Booking confirmation
    └── admin.html            # Admin dashboard
```

## 🛣️ Routes

| Route | Purpose |
|-------|---------|
| `/` | Homepage with service preview |
| `/services` | All photography services |
| `/service/<slug>` | Service details page |
| `/gallery` | Photo gallery with filtering |
| `/booking/<service_slug>` | Booking form for service |
| `/payment/<booking_id>` | Payment page |
| `/reviews` | Client reviews and testimonials |
| `/success/<booking_id>` | Booking confirmation |
| `/admin` | Admin dashboard |
| `/api/book` | Booking API endpoint |
| `/api/pay` | Payment API endpoint |

## 📸 Services Offered

1. **Candid Photography** - ₹10,000+ (8 hrs min)
2. **Wedding Photography** - ₹15,000+ (8 hrs min)
3. **Pre-Wedding Shoots** - ₹12,000+ (4 hrs min)
4. **Event Photography** - ₹8,000+ (4 hrs min)
5. **Birthday Photography** - ₹5,000+ (2 hrs min)
6. **Portrait Sessions** - ₹5,000+ (1 hr min)

Extra hours: ₹2,000 per hour

## 🎨 Color Theme

The website supports light and dark themes. Colors are defined as CSS variables:

- **Dark Theme**: Dark backgrounds with bright accents
- **Light Theme**: Light backgrounds with purple accents
- **Accent Color**: Gold yellow (#e8ff5a) in dark, Purple (#5b3ef8) in light

## 📝 Database Schema

### Bookings Table
- ID, Customer Name, Phone, Email
- Service ID, Service Name, Booking Date
- Duration, Event Address, Event Type
- Special Requests, Total Price
- Payment Status, Booking Status
- Latitude, Longitude, Created At

### Gallery Table
- ID, Title, Image Path
- Service Type, Description
- Uploaded At

### Reviews Table
- ID, Customer Name, Service Type
- Rating (1-5), Review Text
- Is Approved, Created At

## 🔧 Customization

### Update Business Info
Edit in `templates/base.html`:
- Phone number
- Business location
- Branding

### Update Services
Edit `PHOTOGRAPHY_SERVICES` list in `app.py`:
- Add/remove services
- Change pricing
- Update descriptions

### Add Gallery Images
1. Add images to `static/gallery/`
2. Update `GALLERY_ITEMS` in `app.py`

## 💳 Payment Integration

The payment system is ready for integration with:

### Razorpay (For Indian customers)
```python
# TODO: Implement Razorpay integration
# Need to add: Razorpay API keys, SDK integration
```

### Stripe (International)
```python
# TODO: Implement Stripe integration
# Need to add: Stripe API keys, SDK integration
```

Currently, it accepts bookings with manual payment following up.

## 📊 Admin Features

- View all bookings with filters
- Monitor payment status
- Track booking status
- Approve/manage customer reviews
- View revenue statistics
- Export booking data

## 🚀 Deployment

### Deploy to Heroku

1. Create `Procfile`:
```
web: python app.py
```

2. Create `runtime.txt`:
```
python-3.11.0
```

3. Deploy:
```bash
git push heroku main
```

### Deploy to PythonAnywhere

1. Upload files via Git or FTP
2. Create web app with Flask
3. Point to `app.py`
4. Reload

## 🐛 Troubleshooting

**Port already in use**
```bash
python app.py --port 5001
```

**Database errors**
- Delete `database.db` and restart (recreates schema)

**Static files not loading**
- Check `static/` folder exists with CSS files
- Verify paths in templates use `{{ url_for() }}`

## 📧 Contact

For booking inquiries and photography services:
- **Business**: Crazy Vision
- **Location**: Ballari, Karnataka
- **Services**: Professional candid, wedding, event, and portrait photography

## 📄 License

This website template is provided as-is for photography business use.

---

**Made with ❤️ for photographers**
