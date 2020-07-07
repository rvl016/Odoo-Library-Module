
from odoo import fields, models, api

class Category( models.Model) :

  _name = "library.category"
  _description = "Books categories"


  name = fields.Char( string = "Category Name", required = True)
  books_ids = fields.One2many( string = "Books", comodel_name = "library.book",
    inverse_name = "category_id")
  books_in_category = fields.Integer( string = "Books titles quantity", 
    compute = "_get_titles_number")

  @api.depends( "books_ids")
  def _get_titles_number( self) :
    for category in self :
      category.books_in_category = len( category.books_ids)
      #category.books_in_category = category.books_ids.read_group( 
      #  fields = ['name:count_distinct'], groupby = ['name'])