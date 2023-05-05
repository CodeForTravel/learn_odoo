from odoo import models, fields

class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "A simple description about estate property tag model"
    _order = "name"

    name = fields.Char(string='Name', required=True)

    #SQL constraints.
    _sql_constraints = [
        #unique name validation
        ('name_uniq', 'unique (name)', "A tag with the same name already exists."),
    ]