from odoo import models, fields


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Property Model"

    name = fields.Char(string="Name of Property", default="My new house", required=True)
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price",readonly=True, required=False, copy=False)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='State',
        default="new",
        copy=False,
        selection=[('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    salesperson_id = fields.Many2one("res.users", string="Sales Person")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")

    def set_to_sold(self):
        self.state = 'sold'
