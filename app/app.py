import os
import psycopg2
from flask import Flask, jsonify, request

app = Flask(__name__)


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        database=os.getenv("DB_NAME", "orders"),
        user=os.getenv("DB_USER", "shopease"),
        password=os.getenv("DB_PASSWORD", "shopease123"),
    )


@app.route("/")
def home():
    return "ShopEase Order Service - try /api/orders"


@app.route("/api/health")
def health():
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({"status": "ok", "database": "connected"})
    except Exception as e:
        return jsonify({"status": "error", "database": str(e)}), 500


@app.route("/api/orders", methods=["GET"])
def get_orders():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, customer, item, quantity, status
        FROM orders
        ORDER BY id
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    orders = [
        {
            "id": row[0],
            "customer": row[1],
            "item": row[2],
            "quantity": row[3],
            "status": row[4]
        }
        for row in rows
    ]

    return jsonify(orders)


@app.route("/api/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, customer, item, quantity, status
        FROM orders
        WHERE id = %s
    """, (order_id,))

    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        return jsonify({"error": "Order not found"}), 404

    return jsonify({
        "id": row[0],
        "customer": row[1],
        "item": row[2],
        "quantity": row[3],
        "status": row[4]
    })


@app.route("/api/orders", methods=["POST"])
def create_order():
    data = request.get_json()

    customer = data.get("customer")
    item = data.get("item")
    quantity = data.get("quantity")

    if not customer or not item or not quantity:
        return jsonify({
            "error": "customer, item and quantity are required"
        }), 400

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO orders (customer, item, quantity, status)
        VALUES (%s, %s, %s, 'PLACED')
        RETURNING id, customer, item, quantity, status
    """, (customer, item, quantity))

    row = cur.fetchone()

    conn.commit()

    cur.close()
    conn.close()

    return jsonify({
        "id": row[0],
        "customer": row[1],
        "item": row[2],
        "quantity": row[3],
        "status": row[4]
    }), 201


@app.route("/api/orders/<int:order_id>", methods=["PATCH"])
def update_order(order_id):
    data = request.get_json()
    status = data.get("status")

    if not status:
        return jsonify({"error": "status is required"}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE orders
        SET status = %s
        WHERE id = %s
        RETURNING id, customer, item, quantity, status
    """, (status, order_id))

    row = cur.fetchone()

    if not row:
        conn.rollback()
        cur.close()
        conn.close()
        return jsonify({"error": "Order not found"}), 404

    conn.commit()

    cur.close()
    conn.close()

    return jsonify({
        "id": row[0],
        "customer": row[1],
        "item": row[2],
        "quantity": row[3],
        "status": row[4]
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
