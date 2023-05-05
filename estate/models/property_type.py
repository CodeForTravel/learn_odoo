from odoo import models, fields


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "A simple property type model."
    _order = 'sequence, name'

    name = fields.Char(string="Property Type", default="House", required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")

    #SQL constraints.
    _sql_constraints = [
        #unique name validation
        ('name_uniq', 'unique (name)', "A tag with the same name already exists."),
    ]