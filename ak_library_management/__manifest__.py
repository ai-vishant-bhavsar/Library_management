{
    'name': 'Library Management',
    'version': '1.0',
    'category': 'Library',
    'author': 'Vishant Bhavsar',
    'website': 'http://aktivesoftware.com',
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',

        'views/library_book_views.xml',
        'views/library_member_views.xml',
        'views/library_book_category_views.xml',
        'views/library_book_tags_views.xml',
        'views/menu.xml',
    ],

    'installable': True,
    'application': True,
}
