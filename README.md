# Rent a Led Wall in Ballari

# LumenWall — LED Wall Rental Booking System

A full-stack web application for booking LED walls for events.

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
python app.py

# 3. Open browser
http://127.0.0.1:5000
```

## Pages

| Route | Description |
|-------|-------------|
| `/` | Homepage with LED wall listings |
| `/booking/<wall_id>` | Booking form (6x8 or 8x12) |
| `/success/<booking_id>` | Booking confirmation |
| `/admin` | Admin view of all bookings |

## API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| POST | `/api/check-availability` | Check if a wall is free for given dates |
| POST | `/api/book` | Submit a new booking |
| GET | `/api/bookings` | Get all bookings as JSON |

## LED Wall Options

- **6 × 8 ft** — Full HD, 5000 nits, $299/day
- **8 × 12 ft** — 4K Ultra HD, 8000 nits, $499/day

## Features

- ✅ Real-time availability checking
- ✅ Double-booking prevention
- ✅ Interactive Leaflet map with pin drop
- ✅ Reverse geocoding (auto-fills address from map click)
- ✅ Admin dashboard with booking stats
- ✅ SQLite database (zero config)
