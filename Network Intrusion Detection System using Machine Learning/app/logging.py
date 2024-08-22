import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging(app):
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/nids.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('NIDS startup')

def log_packet(packet):
    logging.info(f'Packet detected: ID={packet.id}, Protocol={packet.protocol_type}, Intrusion={packet.is_intrusion}')

def log_alert(alert):
    logging.warning(f'Alert generated: {alert.message} (Severity: {alert.severity})')