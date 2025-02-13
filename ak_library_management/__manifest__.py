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
        'base', 
        'web', 
        'product', 
        'stock',
        'sale'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/action.xml',
        'views/library_views.xml',
        'views/library_member_views.xml',
        'views/product_template_views.xml',
        'views/menu.xml',
    ],

    'installable': True,
    'application': True,
}
