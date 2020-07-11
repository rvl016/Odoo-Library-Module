
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
  books_in_library = fields.Integer( string = "Books titles in library", 
    compute = "_get_number_of_books")
  times_rented = fields.Integer( string = 
    "Times the author's book has been rented", compute = "_get_times_rented")

  books_ids = fields.Many2many( comodel_name = "library.book", 
    relation = "authors_book", column1 = "author_id", 
    column2 = "book_id", string = "Author's books")

  def _get_number_of_books( self) :
    for author in self :
      book_titles = author.books_ids.mapped( 'title')
      author.books_in_library = len( set( book_titles))

  def _get_times_rented( self) :
    for author in self :
      sql = "SELECT COUNT(*) FROM authors_book INNER JOIN library_author "\
        "ON authors_book.author_id = library_author.id "\
        "INNER JOIN library_rent ON authors_book.book_id = "\
        "library_rent.book_id WHERE library_author.id = %s"
      author.env.cr.execute( sql, (author.id,))
      author.times_rented = author.env.cr.dictfetchone()['count']