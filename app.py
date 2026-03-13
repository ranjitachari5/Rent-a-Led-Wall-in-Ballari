from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
DATABASE = 'database.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Photography Services table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS photo_services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            slug TEXT NOT NULL UNIQUE,
            description TEXT NOT NULL,
            base_price INTEGER NOT NULL,
            includes TEXT,
            min_hours INTEGER,
            category TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Bookings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            service_id INTEGER NOT NULL,
            service_name TEXT NOT NULL,
            booking_date TEXT NOT NULL,
            duration_hours INTEGER NOT NULL,
            event_address TEXT NOT NULL,
            event_type TEXT,
            special_requests TEXT,
            total_price INTEGER,
            payment_status TEXT DEFAULT 'unpaid',
            booking_status TEXT DEFAULT 'pending',
            latitude REAL,
            longitude REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(service_id) REFERENCES photo_services(id)
        )
    ''')
    
    # Gallery table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gallery (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            image_path TEXT NOT NULL,
            service_type TEXT,
            description TEXT,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Reviews/Testimonials table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            service_type TEXT,
            rating INTEGER,
            review_text TEXT NOT NULL,
            is_approved INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

# Photography Services data
PHOTOGRAPHY_SERVICES = [
    {
        'id': 1,
        'name': 'Candid Photography',
        'slug': 'candid',
        'description': 'Natural and unposed moments captured beautifully. Perfect for capturing genuine emotions and authentic moments at any event.',
        'base_price': 10000,
        'includes': ['500+ edited photos', 'Digital gallery', 'Same day album'],
        'min_hours': 8,
        'category': 'photography'
    },
    {
        'id': 2,
        'name': 'Wedding Photography',
        'slug': 'wedding',
        'description': 'Professional coverage of your complete wedding - from pre-wedding to reception. Preserve every precious moment of your special day.',
        'base_price': 15000,
        'includes': ['Full day coverage', '2000+ curated photos', 'Digital album', 'Prints included'],
        'min_hours': 8,
        'category': 'wedding'
    },
    {
        'id': 3,
        'name': 'Pre-Wedding Shoots',
        'slug': 'pre-wedding',
        'description': 'Beautiful couple portraits and romantic moments before the big day. Multiple locations and professional styling included.',
        'base_price': 12000,
        'includes': ['Outdoor locations', '300+ edited photos', 'Digital album', 'Prints'],
        'min_hours': 4,
        'category': 'wedding'
    },
    {
        'id': 4,
        'name': 'Event Photography',
        'slug': 'events',
        'description': 'Corporate events, conferences, and celebrations covered professionally. All important moments documented.',
        'base_price': 8000,
        'includes': ['300+ photos', 'Digital delivery', 'Quick editing', 'Print ready files'],
        'min_hours': 4,
        'category': 'events'
    },
    {
        'id': 5,
        'name': 'Birthday Photography',
        'slug': 'birthday',
        'description': 'Capture the joy and laughter of birthday celebrations. From children to adult parties, we cover it all.',
        'base_price': 5000,
        'includes': ['200+ photos', 'Digital album', 'Same day delivery', 'Prints'],
        'min_hours': 2,
        'category': 'birthday'
    },
    {
        'id': 6,
        'name': 'Portrait Sessions',
        'slug': 'portraits',
        'description': 'Professional individual, couple, or family portraits. Studio or outdoor location with professional styling.',
        'base_price': 5000,
        'includes': ['100+ photos', 'Best shots edited', 'Digital delivery', '20x30 print'],
        'min_hours': 1,
        'category': 'portraits'
    }
]

# Sample gallery data - these would be actual image files
GALLERY_ITEMS = [
    {'id': 1, 'title': 'Wedding Bliss', 'image_path': 'static/gallery/wedding1.jpg', 'service_type': 'Wedding', 'description': 'Beautiful wedding day capture'},
    {'id': 2, 'title': 'Candid Moment', 'image_path': 'static/gallery/candid1.jpg', 'service_type': 'Candid', 'description': 'Natural moment captured'},
    {'id': 3, 'title': 'Birthday Joy', 'image_path': 'static/gallery/birthday1.jpg', 'service_type': 'Birthday', 'description': 'Birthday celebration'},
    {'id': 4, 'title': 'Event Coverage', 'image_path': 'static/gallery/event1.jpg', 'service_type': 'Events', 'description': 'Professional event coverage'},
    {'id': 5, 'title': 'Family Portrait', 'image_path': 'static/gallery/portrait1.jpg', 'service_type': 'Portraits', 'description': 'Family portrait session'},
    {'id': 6, 'title': 'Pre-Wedding', 'image_path': 'static/gallery/prewedding1.jpg', 'service_type': 'Pre-Wedding', 'description': 'Pre-wedding shoot'},
]


# ============ ROUTES ============

@app.route('/')
def index():
    return render_template('index.html', services=PHOTOGRAPHY_SERVICES)

@app.route('/services')
def services():
    return render_template('services.html', services=PHOTOGRAPHY_SERVICES)

@app.route('/service/<service_slug>')
def service_detail(service_slug):
    service = next((s for s in PHOTOGRAPHY_SERVICES if s['slug'] == service_slug), None)
    if not service:
        return redirect(url_for('services'))
    return render_template('service-detail.html', service=service)

@app.route('/gallery')
def gallery():
    return render_template('gallery.html', gallery=GALLERY_ITEMS)

@app.route('/booking/<service_slug>')
def booking(service_slug):
    service = next((s for s in PHOTOGRAPHY_SERVICES if s['slug'] == service_slug), None)
    if not service:
        return redirect(url_for('services'))
    return render_template('booking.html', service=service)

@app.route('/api/book', methods=['POST'])
def book():
    data = request.json
    required = ['customer_name', 'phone', 'service_id', 'booking_date', 'duration_hours', 'event_address']
    if not all(data.get(f) for f in required):
        return jsonify({'success': False, 'message': 'All fields are required.'})

    try:
        duration_hours = int(data['duration_hours'])
        service = next((s for s in PHOTOGRAPHY_SERVICES if s['id'] == int(data['service_id'])), None)
        
        if not service:
            return jsonify({'success': False, 'message': 'Invalid service selected.'})
        
        if duration_hours < service['min_hours']:
            return jsonify({'success': False, 'message': f'Minimum duration is {service["min_hours"]} hours.'})
        
        # Calculate total price
        total_price = service['base_price'] + ((duration_hours - service['min_hours']) * 2000)

        conn = get_db()
        conn.execute('''
            INSERT INTO bookings 
            (customer_name, phone, email, service_id, service_name, booking_date, duration_hours, 
             event_address, event_type, special_requests, total_price, latitude, longitude)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['customer_name'], data['phone'], data.get('email'), data['service_id'],
            service['name'], data['booking_date'], duration_hours, data['event_address'],
            data.get('event_type'), data.get('special_requests'), total_price,
            data.get('latitude'), data.get('longitude')
        ))
        conn.commit()
        booking_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        conn.close()

        return jsonify({'success': True, 'booking_id': booking_id, 'total_price': total_price})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/success/<int:booking_id>')
def success(booking_id):
    conn = get_db()
    booking = conn.execute('SELECT * FROM bookings WHERE id = ?', (booking_id,)).fetchone()
    conn.close()
    if not booking:
        return redirect(url_for('index'))
    return render_template('success.html', booking=booking)

@app.route('/payment/<int:booking_id>')
def payment(booking_id):
    conn = get_db()
    booking = conn.execute('SELECT * FROM bookings WHERE id = ?', (booking_id,)).fetchone()
    conn.close()
    if not booking:
        return redirect(url_for('index'))
    return render_template('payment.html', booking=booking)

@app.route('/api/pay', methods=['POST'])
def pay():
    """Handle payment processing (Razorpay/Stripe integration)"""
    data = request.json
    booking_id = data.get('booking_id')
    payment_method = data.get('payment_method')  # 'razorpay' or 'stripe'
    
    conn = get_db()
    booking = conn.execute('SELECT * FROM bookings WHERE id = ?', (booking_id,)).fetchone()
    conn.close()
    
    if not booking:
        return jsonify({'success': False, 'message': 'Booking not found.'})
    
    # For now, mark as paid. In production, verify with payment gateway
    conn = get_db()
    conn.execute('UPDATE bookings SET payment_status = ? WHERE id = ?', ('paid', booking_id))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Payment processed successfully.'})

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    if request.method == 'POST':
        data = request.json
        required = ['customer_name', 'service_type', 'rating', 'review_text']
        if not all(data.get(f) for f in required):
            return jsonify({'success': False, 'message': 'All fields are required.'})
        
        try:
            rating = int(data['rating'])
            if rating < 1 or rating > 5:
                return jsonify({'success': False, 'message': 'Rating must be between 1 and 5.'})
            
            conn = get_db()
            conn.execute('''
                INSERT INTO reviews (customer_name, service_type, rating, review_text, is_approved)
                VALUES (?, ?, ?, ?, ?)
            ''', (data['customer_name'], data['service_type'], rating, data['review_text'], 0))
            conn.commit()
            conn.close()
            
            return jsonify({'success': True, 'message': 'Review submitted! It will be approved soon.'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})
    
    conn = get_db()
    approved_reviews = conn.execute('SELECT * FROM reviews WHERE is_approved = 1 ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('reviews.html', reviews=approved_reviews)

@app.route('/admin')
def admin():
    conn = get_db()
    bookings = conn.execute('SELECT * FROM bookings ORDER BY created_at DESC').fetchall()
    pending_reviews = conn.execute('SELECT * FROM reviews WHERE is_approved = 0 ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('admin.html', bookings=bookings, pending_reviews=pending_reviews)

@app.route('/api/bookings')
def api_bookings():
    conn = get_db()
    bookings = conn.execute('SELECT * FROM bookings ORDER BY created_at DESC').fetchall()
    conn.close()
    return jsonify([dict(b) for b in bookings])

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
