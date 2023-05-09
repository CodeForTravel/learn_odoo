import datetime
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class PropertyOffer(models.Model):
   _name = "estate.property.offer"
   _description = "A simple description about property offer"
   _order = "price desc"

   price = fields.Float()
   status = fields.Selection(
       copy=False,
       selection=[("accepted", "Accepted"), ("refused", "Refused")]
   )
   partner_id = fields.Many2one("res.partner", required=True)
   property_id = fields.Many2one("estate.property", required=True)
   property_type_id = fields.Many2one(
       related="property_id.property_type_id",
       string="Property Type",
       store=True
   )
   
   date_deadline = fields.Date(
      compute="_compute_date_deadline",
      inverse='_inverse_date_deadline',
      index=True,
      readonly=False, store=True
   )

   validity = fields.Integer(default=7)

   #compute method
   @api.depends("create_date", "validity")
   def _compute_date_deadline(self):
      for record in self:
         if record.create_date:
            record.date_deadline = record.create_date + datetime.timedelta(days=record.validity)
         else:
            record.date_deadline = datetime.datetime.now() + datetime.timedelta(days=record.validity)

   #inverse compute method
   def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

   #action
   def action_offer_accepted(self):
      for offer in self:
         offer.status = "accepted"
         # set selling price to property model
         offer.property_id.selling_price = offer.price
         # set buyer to property model
         offer.property_id.buyer_id = offer.partner_id
         offer.property_id.state = 'offer accepted'
         return {
            'effect': {
               'fadeout': 'slow',
               'message': "Offer accepted successfully",
               'type': 'rainbow_man',
            }
         }

   #action
   def action_offer_refused(self):
      for offer in self:
         offer.status = "refused"
         return {
            'effect': {
               'fadeout': 'slow',
               'message': "Offer Refused successfully",
               'type': 'rainbow_man',
            }
         }
      
   #SQL constraints.
   _sql_constraints = [
        ('check_price', 'CHECK(price > 0)',
         'The offer price of a property must be greater than 0!'),
    ]
   
   @api.model
   def create(self, vals):
      """
      At offer creation, set the property state to ‘Offer Received’. Also raise an error if the user tries to create an offer with a lower amount than an existing offer.
      """
      existing_offer = self.env['estate.property.offer'].search([
         ('property_id', '=', vals.get('property_id')),
         ('price', '>', vals.get('price'))
      ])

      if existing_offer:
         raise ValidationError("Cannot create an offer with a lower amount than an existing offer.")
      
      offer = super().create(vals)
      offer.property_id.state = 'offer received'
      return offer