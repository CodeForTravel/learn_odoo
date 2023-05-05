from odoo import models, fields


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "A simple property type model."

    name = fields.Char(string="Property Type", default="House", required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")

    #SQL constraints.
    _sql_constraints = [
        #unique name validation
        ('name_uniq', 'unique (name)', "A tag with the same name already exists."),
    ]