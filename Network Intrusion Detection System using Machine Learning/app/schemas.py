from marshmallow import Schema, fields

class PacketSchema(Schema):
    id = fields.Int(dump_only=True)
    timestamp = fields.DateTime(dump_only=True)
    protocol_type = fields.Str()
    is_intrusion = fields.Boolean()
    header_length = fields.Int()
    duration = fields.Float()
    rate = fields.Float()

class AlertSchema(Schema):
    id = fields.Int(dump_only=True)
    timestamp = fields.DateTime(dump_only=True)
    message = fields.Str()
    severity = fields.Str()