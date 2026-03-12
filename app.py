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
    conn.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            led_wall_size TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            event_address TEXT NOT NULL,
            latitude REAL,
            longitude REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

LED_WALLS = [
    {
        'id': '6x8',
        'size': '6 × 8 ft',
        'width': 6,
        'height': 8,
        'description': 'Perfect for intimate gatherings, corporate meetings, and small events.',
        'pixels': '1920 × 1080',
        'brightness': '5000 nits',
        'price': '$299/day',
        'features': ['Full HD Resolution', 'Indoor/Outdoor', 'Quick Setup', 'Remote Control']
    },
    {
        'id': '8x12',
        'size': '8 × 12 ft',
        'width': 8,
        'height': 12,
        'description': 'Ideal for large events, concerts, trade shows, and outdoor festivals.',
        'pixels': '3840 × 2160',
        'brightness': '8000 nits',
        'price': '$499/day',
        'features': ['4K Ultra HD', 'Weather Resistant', 'Professional Grade', 'Wireless Sync']
    }
]

@app.route('/')
def index():
    return render_template('index.html', led_walls=LED_WALLS)

@app.route('/booking/<wall_id>')
def booking(wall_id):
    wall = next((w for w in LED_WALLS if w['id'] == wall_id), None)
    if not wall:
        return redirect(url_for('index'))
    return render_template('booking.html', wall=wall)

@app.route('/api/check-availability', methods=['POST'])
def check_availability():
    data = request.json
    wall_size = data.get('led_wall_size')
    start_date = data.get('start_date')
    end_date = data.get('end_date')

    if not all([wall_size, start_date, end_date]):
        return jsonify({'available': False, 'message': 'Missing required fields'})

    conn = get_db()
    conflict = conn.execute('''
        SELECT id FROM bookings
        WHERE led_wall_size = ?
        AND NOT (end_date < ? OR start_date > ?)
    ''', (wall_size, start_date, end_date)).fetchone()
    conn.close()

    if conflict:
        return jsonify({'available': False, 'message': 'This LED wall is already booked for the selected dates.'})
    return jsonify({'available': True, 'message': 'Available for booking!'})

@app.route('/api/book', methods=['POST'])
def book():
    data = request.json
    required = ['customer_name', 'phone', 'led_wall_size', 'start_date', 'end_date', 'event_address']
    if not all(data.get(f) for f in required):
        return jsonify({'success': False, 'message': 'All fields are required.'})

    # Double-check availability
    conn = get_db()
    conflict = conn.execute('''
        SELECT id FROM bookings
        WHERE led_wall_size = ?
        AND NOT (end_date < ? OR start_date > ?)
    ''', (data['led_wall_size'], data['start_date'], data['end_date'])).fetchone()

    if conflict:
        conn.close()
        return jsonify({'success': False, 'message': 'This LED wall was just booked. Please choose different dates.'})

    conn.execute('''
        INSERT INTO bookings (customer_name, phone, led_wall_size, start_date, end_date, event_address, latitude, longitude)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['customer_name'], data['phone'], data['led_wall_size'],
        data['start_date'], data['end_date'], data['event_address'],
        data.get('latitude'), data.get('longitude')
    ))
    conn.commit()
    booking_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
    conn.close()

    return jsonify({'success': True, 'booking_id': booking_id})

@app.route('/success/<int:booking_id>')
def success(booking_id):
    conn = get_db()
    booking = conn.execute('SELECT * FROM bookings WHERE id = ?', (booking_id,)).fetchone()
    conn.close()
    if not booking:
        return redirect(url_for('index'))
    return render_template('success.html', booking=booking)

@app.route('/admin')
def admin():
    conn = get_db()
    bookings = conn.execute('SELECT * FROM bookings ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('admin.html', bookings=bookings)

@app.route('/api/bookings')
def api_bookings():
    conn = get_db()
    bookings = conn.execute('SELECT * FROM bookings ORDER BY created_at DESC').fetchall()
    conn.close()
    return jsonify([dict(b) for b in bookings])

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
