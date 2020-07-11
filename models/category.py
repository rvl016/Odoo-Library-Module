
from odoo import fields, models, api

class Category( models.Model) :

  _name = "library.category"
  _description = "Books categories"


  name = fields.Char( string = "Category Name", required = True)
  books_ids = fields.One2many( string = "Books", comodel_name = "library.book",
    inverse_name = "category_id")
  books_in_category = fields.Integer( string = "Books titles quantity", 
    compute = "_get_titles_number")

  def _get_titles_number( self) :
    for category in self :
      records = category.env['library.book'].search( 
        args = [('category_id', '=', category.id)])
      category.books_in_category = len( set( records.mapped( 'title')))