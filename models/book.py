
from odoo import models, fields, api

class Book( models.Model) :

  _description = "Book"
  _name = "library.book"
  _order = "name"

  _sql_constraints = [
    ("edition_positive_int", "CHECK( edition > 0)", 
      "Edition should be at least the first."),
    ("isbn_valid", "CHECK( isbn ~* '^[0-9]{13}$')", 
      "ISBN should be in standard format.")
  ]

  name = fields.Char( string = "Book Title", required = True)
  editor = fields.Char( string = "Editor", default = "None")
  edition = fields.Integer( string = "Edition", default = 1)
  isbn = fields.Char( string = "ISBN", size = 13, required = True)
  times_rented = fields.Integer( string = "Times Rented", 
    compute = "_getTimesRented", readonly = True)
  available = fields.Boolean( string = "Available", 
    compute = "_getAvailability", readonly = True)

  category_id = fields.Many2one( string = "Category", 
    comodel_name = "library.category", ondelete = "cascade", 
    required = True)

  authors_ids = fields.Many2many( comodel_name = "library.author", 
    relation = "authors_book", column1 = "book_id", 
    column2 = "author_id", string = "Authors", required = True)

  rents_ids = fields.One2many( comodel_name = "library.rent", 
    inverse_name = "book_id")

  @api.depends( "rents_ids")
  def _getTimesRented( self) :
    for book in self :
      book.times_rented = len( book.rents_ids)

  @api.depends( "rents_ids")
  def _getAvailability( self) :
    for book in self :
      print( book.rents_ids.mapped( 'status'))
      book.available = all( 
        status == "Finalized" for status in book.rents_ids.mapped( 'status'))

  @api.constrains( "authors_ids")
  def _has_book_at_least_one_author( self) :
    for book in self :
      if len( book.authors_ids) == 0 :
        raise ValidationError( "A book should have at least one author.")

