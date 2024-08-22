from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Packet(Base):
    __tablename__ = 'packets'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    flow_duration = Column(Float)
    header_length = Column(Integer)
    protocol_type = Column(String(10))
    duration = Column(Float)
    rate = Column(Float)
    fin_flag_number = Column(Integer)
    syn_flag_number = Column(Integer)
    rst_flag_number = Column(Integer)
    psh_flag_number = Column(Integer)
    ack_flag_number = Column(Integer)
    ece_flag_number = Column(Integer)
    cwr_flag_number = Column(Integer)
    ack_count = Column(Integer)
    syn_count = Column(Integer)
    fin_count = Column(Integer)
    urg_count = Column(Integer)
    rst_count = Column(Integer)
    is_intrusion = Column(Boolean)

class Alert(Base):
    __tablename__ = 'alerts'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    message = Column(String(200))
    severity = Column(String(20))
    packet_id = Column(Integer, ForeignKey('packets.id'))
    packet = relationship("Packet")