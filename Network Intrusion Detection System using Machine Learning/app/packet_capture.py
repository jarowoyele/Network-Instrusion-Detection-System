from scapy.all import sniff, IP, TCP, UDP, conf
from app.models import Packet, Alert, Base
from app.ml_model import model
from app import engine, Session
from app.logging import log_packet, log_alert
import time
import pandas as pd

Base.metadata.create_all(engine)

def extract_features(packet):
    features = {
        'flow_duration': time.time() - packet.time,
        'Header_Length': len(packet),
        'Protocol Type': packet[IP].proto,
        'Duration': 0,
        'Rate': 0,
        'fin_flag_number': 0,
        'syn_flag_number': 0,
        'rst_flag_number': 0,
        'psh_flag_number': 0,
        'ack_flag_number': 0,
        'ece_flag_number': 0,
        'cwr_flag_number': 0,
        'ack_count': 0,
        'syn_count': 0,
        'fin_count': 0,
        'urg_count': 0,
        'rst_count': 0
    }

    if TCP in packet:
        tcp = packet[TCP]
        features.update({
            'fin_flag_number': int(tcp.flags.F),
            'syn_flag_number': int(tcp.flags.S),
            'rst_flag_number': int(tcp.flags.R),
            'psh_flag_number': int(tcp.flags.P),
            'ack_flag_number': int(tcp.flags.A),
            'ece_flag_number': int(tcp.flags.E),
            'cwr_flag_number': int(tcp.flags.C),
        })
    elif UDP in packet:
        features['Protocol Type'] = 17  # UDP protocol number

    return features

def process_packet(packet):
    if IP in packet:
        features = extract_features(packet)
        
        # Predict intrusion
        is_intrusion = model.predict(features)
        
        session = Session()
        
        # Save to database
        new_packet = Packet(
            flow_duration=features['flow_duration'],
            header_length=features['Header_Length'],
            protocol_type=str(features['Protocol Type']),  # Convert to string
            duration=features['Duration'],
            rate=features['Rate'],
            fin_flag_number=features['fin_flag_number'],
            syn_flag_number=features['syn_flag_number'],
            rst_flag_number=features['rst_flag_number'],
            psh_flag_number=features['psh_flag_number'],
            ack_flag_number=features['ack_flag_number'],
            ece_flag_number=features['ece_flag_number'],
            cwr_flag_number=features['cwr_flag_number'],
            ack_count=features['ack_count'],
            syn_count=features['syn_count'],
            fin_count=features['fin_count'],
            urg_count=features['urg_count'],
            rst_count=features['rst_count'],
            is_intrusion=bool(is_intrusion)  # Ensure boolean type
        )
        session.add(new_packet)
        
        if is_intrusion:
            alert = Alert(
                message=f"Potential intrusion detected from {packet[IP].src}",
                severity="High",
                packet=new_packet
            )
            session.add(alert)
            log_alert(alert)

        session.commit()
        log_packet(new_packet)
        session.close()
        
def start_capture(interface=None):
    if interface is None:
        # Get the default interface
        interface = conf.iface

    print(f"Available interfaces: {', '.join(conf.ifaces.data.keys())}")
    print(f"Starting packet capture on interface: {interface}")

    try:
        sniff(iface=interface, prn=process_packet, store=0)
    except OSError as e:
        print(f"Error: {e}")
        print("Please make sure you're running the script with administrator privileges.")
        print("If the error persists, try specifying a different interface.")

if __name__ == "__main__":
    start_capture()