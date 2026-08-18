from marshmallow import Schema, fields


class StudentSchema(Schema):

    id = fields.Integer(dump_only=True)

    name = fields.String(required=True)

    email = fields.Email(required=True)

    course = fields.String(required=True)

    age = fields.Integer(required=True)