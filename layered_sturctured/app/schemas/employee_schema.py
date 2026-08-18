from marshmallow import Schema, fields


class EmployeeSchema(Schema):

    id = fields.Integer(dump_only=True)

    name = fields.String(required=True)

    email = fields.Email(required=True)

    salary = fields.Integer(required=True)