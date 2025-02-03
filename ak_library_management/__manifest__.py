# -*- coding: utf-8 -*-
{
    'name': 'Library Management',
    'version': '18.0.1.0.0',
    'category': 'Library',
    'author': 'Vishant Bhavsar',
    'website': 'http://aktivesoftware.com',
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',

        'views/library_views.xml',
        'views/library_book_views.xml',
        'views/library_member_views.xml',
        'views/library_book_category_views.xml',
        'views/library_book_tags_views.xml',
        'views/menu.xml',
    ],

    'installable': True,
    'application': True,
}