import datetime
from odoo import models, fields, api

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

   date_deadline = fields.Date(
      compute="_compute_date_deadline",
      inverse='_inverse_date_deadline',
      index=True,
      readonly=False, store=True
   )

   validity = fields.Integer(default=7)

   @api.depends("create_date", "validity")
   def _compute_date_deadline(self):
      for record in self:
         if record.create_date:
            record.date_deadline = record.create_date + datetime.timedelta(days=record.validity)
         else:
            record.date_deadline = datetime.datetime.now() + datetime.timedelta(days=record.validity)

   def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days



