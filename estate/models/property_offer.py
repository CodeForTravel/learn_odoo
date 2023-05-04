from odoo import models, fields

class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "A simple description about property offer"

    price = fields.Float()
    status = fields.Selection(
       copy=False,
       default="accepted",
       selection=[("accepted", "Accepted"), ("refused", "Refused")]
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)