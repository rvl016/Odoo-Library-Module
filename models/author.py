
from odoo import models, fields, api

class Author( models.Model) :
  
  _description = "Author"
  _name = "library.author"
  _order = "name"

  _sql_constraints = [
    ("name_unique", "UNIQUE( name)", 
      "There is a author with this name already.")
  ]

  name = fields.Char( string = "Author Name", required = True)
  books_in_library = fields.Integer( string = "Books in library", 
    compute = "_getNumberOfBooks")
  times_rented = fields.Integer( string = 
    "Times the author's book has been rented.", compute = "_getTimesRented")

  books_ids = fields.Many2many( comodel_name = "library.book", 
    relation = "authors_book", column1 = "author_id", 
    column2 = "book_id", string = "Author's books")

  @api.depends( "books_ids")
  def _getNumberOfBooks( self) :
    for author in self :
      author.books_in_library = self.env["library.authors_book"].read_group(
        domain = [("library.author.id", "=", self.id)], 
        groupby = ["library.book.isbn", "library.book.edition"]).count()

  @api.depends( "books_ids")
  def _getTimesRented( self) :
    for author in self :
      author.times_rented = self.env["library.rent"].search( 
        domain = [("library.author.id", "=", self.id)]).count()