from odoo import models, fields

class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "A simple description about estate property tag model"

    name = fields.Char(string='Name', required=True)