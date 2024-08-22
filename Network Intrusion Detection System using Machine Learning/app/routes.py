from flask import Blueprint, render_template, jsonify, request
from app.models import Packet, Alert
from app.schemas import PacketSchema, AlertSchema
from app import Session, limiter
from sqlalchemy import desc
import os

main = Blueprint('main', __name__)

@main.route('/')
def dashboard():
    try:
        return render_template('dashboard.html')
    except Exception as e:
        print(f"Error rendering template: {str(e)}")
        return f"Error: {str(e)}", 500
    
@main.route('/api/packets')
@limiter.limit("100/minute")
def get_packets():
    session = Session()
    packets = session.query(Packet).order_by(desc(Packet.timestamp)).limit(100).all()
    packet_schema = PacketSchema(many=True)
    result = packet_schema.dump(packets)
    session.close()
    return jsonify(result)

@main.route('/api/alerts')
@limiter.limit("100/minute")
def get_alerts():
    session = Session()
    alerts = session.query(Alert).order_by(desc(Alert.timestamp)).limit(10).all()
    alert_schema = AlertSchema(many=True)
    result = alert_schema.dump(alerts)
    session.close()
    return jsonify(result)

@main.route('/api/search')
@limiter.limit("50/minute")
def search_packets():
    query = request.args.get('query', '')
    protocol = request.args.get('protocol', '')
    intrusion = request.args.get('intrusion', '')

    session = Session()
    packets = session.query(Packet)

    if query:
        packets = packets.filter(Packet.id.like(f'%{query}%'))

    if protocol:
        packets = packets.filter(Packet.protocol_type == protocol)

    if intrusion:
        is_intrusion = intrusion.lower() == 'true'
        packets = packets.filter(Packet.is_intrusion == is_intrusion)

    packets = packets.order_by(desc(Packet.timestamp)).limit(100).all()
    packet_schema = PacketSchema(many=True)
    result = packet_schema.dump(packets)
    session.close()
    return jsonify(result)