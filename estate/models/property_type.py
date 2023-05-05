from odoo import models, fields


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "A simple property type model."

    name = fields.Char(string="Property Type", default="House", required=True)

    #SQL constraints.
    _sql_constraints = [
        #unique name validation
        ('name_uniq', 'unique (name)', "A tag with the same name already exists."),
    ]