
from odoo import models, fields, api

class Rent( models.Model) :

  _description = "Book's rent orders"
  _name = "library.rent"
  _order = "start_date DESC"

  _sql_constraints = [
    ("return_after_rent_date", "CHECK( end_date > start_date)", 
      "End date should be after start date.")
  ]

  name = fields.Char( string = "Customer - Book", compute = "_getRentName")
  start_date = fields.Datetime( string = "Rented on", required = True)
  end_date = fields.Datetime( string = "Return Deadline", required = True)
  status = fields.Char( string = "Rent Status", 
    compute = "_getRentStatus", read_only = True)
  returned_date = fields.Datetime( string = "Returned on", default = None)
  customer_id = fields.Many2one( comodel_name = "library.customer",
    ondelete = "set null")
  book_id = fields.Many2one( comodel_name = "library.book", 
    ondelete = "cascade")

  @api.depends( "start_date", "end_date", "returned_date")
  def _getRentStatus( self) :
    for rent in self :
      if rent.returned_date != None :
        rent.status = "Finalized"
      elif fields.Datetime.now() > rent.end_date :
        rent.status = "Overdue"
      else :
        rent.status = "In time"

  @api.depends( "customer_id", "book_id")
  def _getRentName( self) :
    for rent in self :
      customer_name = rent.customer_id.name or "Unknown Customer"
      book_name = rent.book_id.name or "Unknown Book"
      rent.name = f"{ customer_name } - { book_name }"

  @api.model
  def create( self, newRecordsValues) :
    for newRecordValues in newRecordsValues :
      newRecordValues["start_date"] = fields.Datetime.now()
    return super( Rent, self).create( newRecordsValues)

  @api.model
  def toogleReturned( self) :
    for record in self :
      if record.returned_date == None :
        record.returned_date = fields.Datetime.now()
      else :
        record.returned_date = None
    self.flush()
