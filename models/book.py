
from odoo import models, fields, api
from odoo.exceptions import ValidationError

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

  name = fields.Char( compute = "_get_book_identification", readonly = True,
    string = "Book Identification")
  title = fields.Char( string = "Book Title", required = True)
  editor = fields.Char( string = "Editor", default = "None")
  edition = fields.Integer( string = "Edition", default = 1)
  copy_number = fields.Integer( string = "Copy Number", 
    compute = "_get_copy_number", store = True)
  isbn = fields.Char( string = "ISBN", size = 13, required = True)
  times_rented = fields.Integer( string = "Times Rented", 
    compute = "_get_times_rented", readonly = True)
  available = fields.Boolean( string = "Available", 
    compute = "_get_availability", readonly = True)

  category_id = fields.Many2one( string = "Category", 
    comodel_name = "library.category", ondelete = "cascade", 
    required = True)

  authors_ids = fields.Many2many( comodel_name = "library.author", 
    relation = "authors_book", column1 = "book_id", 
    column2 = "author_id", string = "Authors", required = True,
    copy = True)

  rents_ids = fields.One2many( comodel_name = "library.rent", 
    inverse_name = "book_id", copy = False)

  def register_new_copy( self) :
    for book in self :
      book.copy()

  def get_availability( self) :
    for book in self :
      book._get_availability()
      return book.available

  @api.depends( "title", "edition", "copy_number")
  def _get_book_identification( self) :
    for book in self :
      book.name = f"{ book.title }, Ed. { book.edition } (Copy "\
        f"{ book.copy_number })"

  @api.depends( "isbn", "copy_number")
  def _get_copy_number( self) :
    for book in self :
      copies = book.search( args = [('isbn', '=', book.isbn)])
      copies_numbers = copies.mapped( "copy_number")
      copy_highest = max( copies_numbers) if copies_numbers else 0
      book.copy_number = copy_highest + 1

  @api.depends( "rents_ids")
  def _get_times_rented( self) :
    for book in self :
      book.times_rented = len( book.rents_ids)

  @api.depends( "rents_ids")
  def _get_availability( self) :
    for book in self :
      book.available = all( 
        status == "Finalized" for status in book.rents_ids.mapped( 'status'))
      print( book.name, book.rents_ids.mapped( 'status'))

  @api.constrains( "authors_ids")
  def _has_book_at_least_one_author( self) :
    for book in self :
      if len( book.authors_ids) == 0 :
        raise ValidationError( "A book should have at least one author.")

