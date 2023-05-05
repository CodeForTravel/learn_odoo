import datetime
from odoo import models, fields, api

class PropertyOffer(models.Model):
   _name = "estate.property.offer"
   _description = "A simple description about property offer"
   _order = "price desc"

   price = fields.Float()
   status = fields.Selection(
       copy=False,
       default="accepted",
       selection=[("accepted", "Accepted"), ("refused", "Refused")]
   )
   partner_id = fields.Many2one("res.partner", required=True)
   property_id = fields.Many2one("estate.property", required=True)

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
