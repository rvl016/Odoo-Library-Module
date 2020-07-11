# -*- coding: utf-8 -*-
{
    'name': "library",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'installable': True,
    'application': True,
    'sequence': 1, 

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/security_groups.xml',
        'security/security_rules.xml',
        'security/ir.model.access.csv',

        'views/category_view.xml',
        'views/book_view.xml',
        'views/customer_view.xml',
        'views/rent_view.xml',
        'views/author_view.xml',
        'views/library_actions.xml',
        'views/library_menu.xml',

        'data/category_data.xml',
        'data/author_data.xml',
        'data/book_data.xml',
        'data/customer_data.xml',
        'data/rents_data.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
