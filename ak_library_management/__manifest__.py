# -*- coding: utf-8 -*-
# This is an information file of the module
{
    'name': 'Library Management',
    'version': '18.0.1.0.0',
    'category': 'Library',
    'author': 'Vishant Bhavsar',
    'website': 'http://aktivesoftware.com',
    'license':'LGPL-3',
    'description': 'The Library management system',
    'depends': [
        'stock',
        'sale_management'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence.xml',
        'views/sale_order_views.xml',
        'views/library_views.xml',
        'views/library_member_views.xml',
        'views/library_book_category_views.xml',
        'views/library_book_tags_views.xml',
        'views/product_template_views.xml',
        'views/update_quotations_menu_action_name.xml',
        'views/library_bulk_upload_books_view.xml',
        'views/res_users_view.xml',
        'views/menu.xml',
    ],

    'installable': True,
    'application': True,
}
