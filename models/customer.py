
from odoo import models, fields, api

class Customer( models.Model) :

  _description = "Customer"
  _name = "library.customer"
  _order = "overdue_rents DESC"

  name = fields.Char( string = "Name", required = True)
  registered_on = fields.Datetime( string = "Registered on", 
    compute = "_getRegisteredDate", store = True)
  total_rents = fields.Integer( string = "Number of Rents",
    compute = "_getTotalRents")
  overdue_rents = fields.Integer( string = "Number of Overdue Rents", 
    compute = "_getOverdueRents", store = False)

  rents_ids = fields.One2many( comodel_name = "library.rent", 
    inverse_name = "customer_id")

  @api.depends( "rents_ids")
  def _getTotalRents( self) :
    for customer in self :
      customer.total_rents = len( customer.rents_ids)

  @api.depends( "rents_ids")
  def _getOverdueRents( self) :
    for customer in self :
      custumer.overdue_rents = customer.rents_ids.search( 
        domain = ["rent.status", "=", "Overdue"]).count()

  def _getRegisteredDate( self) :
    for customer in self :
      customer.registered_on = fields.Datetime.now()