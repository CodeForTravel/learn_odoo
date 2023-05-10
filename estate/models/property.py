from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Property Model"
    _order = "id desc"
    
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
    offer_ids = fields.One2many("estate.property.offer", "property_id")

    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")
    # user_id = fields.Many2one("res.users", string="User")

    #computed method
    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area
    
    #computed method
    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if not record.offer_ids:
                record.best_price = None
            else:
                record.best_price = max(p.price for p in record.offer_ids if hasattr(p, 'price'))
   
    #onchange method
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
   
            self.garden_orientation = ""

    #model action
    def sold_property_action(self):
        message = ""
        for property in self:
            if property.state == "canceled":
                message = "cancelled property cannot sold"
            else:
                property.state = "sold"
                return {
                    'effect': {
                        'fadeout': 'slow',
                        'message': "Property sold successfully",
                        'type': 'rainbow_man',
                    }
                }
        if message:
            raise UserError(message)
        return True

    #model action
    def cancel_property_action(self):
        message = ""
        for property in self:
            if property.state == "sold":
                message = "sold  property cannot cancelled"
            else:
                property.state = "canceled"
                return {
                    'effect': {
                        'fadeout': 'slow',
                        'message': "Property cancelled successfully",
                        'type': 'rainbow_man',
                    }
                }
        if message:
            raise UserError(message)
        return True


    #SQL constraints.
    _sql_constraints = [
        #expected_price validation
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'The expected price of a property must be greater than 0!'),
        #selling_price validation
        ('check_selling_price', 'CHECK(selling_price >= 0)',
         'The selling price of a property must be positive')
    ]

    #python constraints.
    @api.constrains('selling_price')
    def _check_selling_price(self):
        """
        Add a constraint so that the selling price cannot be lower than 90% of 
        the expected price.

        """
        for record in self:
            if record.selling_price < (0.9 * record.expected_price):
                raise ValidationError(
                    "Selling price cannot be lower than 90% of the expected price!"
                )
            
    @api.ondelete(at_uninstall=True)
    def check_delete_condition(self):
        for property in self:
            if property.state not in ['new', 'canceled']:
                raise UserError("Only 'New' or 'Canceled' property can be deleted!")
