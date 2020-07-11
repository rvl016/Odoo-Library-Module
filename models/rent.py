
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Rent( models.Model) :

  _description = "Book's rent orders"
  _name = "library.rent"
  _order = "start_date DESC"

  _sql_constraints = [
    ("return_after_rent_date", "CHECK( end_date > start_date)", 
      "End date should be after start date.")
  ]

  name = fields.Char( string = "Customer - Book", compute = "_get_rent_name")
  start_date = fields.Datetime( string = "Rented on", required = True, 
    default = lambda self: fields.Datetime.now())
  end_date = fields.Datetime( string = "Return Deadline", required = True)
  status = fields.Char( string = "Rent Status", 
    compute = "_get_rent_status", readonly = True)
  returned_date = fields.Datetime( string = "Returned on", default = None)
  customer_id = fields.Many2one( comodel_name = "library.customer",
    ondelete = "set null")
  book_id = fields.Many2one( comodel_name = "library.book", 
    ondelete = "cascade")
  book_copy_number = fields.Integer( string = "Book Copy Number", 
    related = "book_id.copy_number")
  book_title = fields.Char( string = "Book Title", related = 'book_id.title')
  book_edition = fields.Integer( string = "Book Edition", 
    related = 'book_id.edition')
  customer_name = fields.Char( string = "Customer", 
    related = 'customer_id.name')

  @api.model
  def create( self, newRecordsValues) :
    self._enforce_book_availability( newRecordsValues['book_id'])
    self._enforce_book_availability( newRecordsValues['book_id'])
    return super( Rent, self).create( newRecordsValues)

  def toggle_returned( self) :
    for book in self :
      if book.returned_date :
        book.set_returned( False)
      else :
        book.set_returned( True)

  @api.model
  def set_returned( self, returned_status) :
    for record in self :
      if returned_status :
        record.returned_date = fields.Datetime.now()
      else :
        record.returned_date = None

  def _enforce_book_availability( self, book_id) :
    book = self.env['library.book'].browse( book_id)
    if not book.get_availability() :
      raise ValidationError( "This book is not available!")

  def _enforce_no_customer_overdues( self, customer_id) :
    customer = self.env['library.customer'].browse( customer_id)
    if customer.overdue_rents > 0 :
      raise ValidationError( "This Customer has overdue rents!")

  @api.depends( "end_date", "returned_date")
  def _get_rent_status( self) :
    now = fields.Datetime.now()
    for rent in self :
      if rent.returned_date :
        rent.status = "Finalized"
      elif rent.end_date and now > rent.end_date :
        rent.status = "Overdue"
      else :
        rent.status = "In time"

  @api.depends( "customer_id", "book_id")
  def _get_rent_name( self) :
    for rent in self :
      customer_name = rent.customer_id.name or "Unknown Customer"
      book_name = rent.book_id.name or "Unknown Book"
      rent.name = f"{ customer_name } - { book_name }"
