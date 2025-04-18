# -*- coding: utf-8 -*-
# This is an information file of the module
{
    'name': 'CRM customisation',
    'version': '18.0.1.0.0',
    'category': 'Customizations',
    'author': 'Vishant Bhavsar',
    'website': 'http://aktivesoftware.com',
    'license': 'LGPL-3',
    'description': 'CRM customisation',
    'depends': [
        'sale_management',
        'stock',
        'purchase',
        'mrp',
        'crm',
        'project'
    ],
    'data': [
        'views/sale_order_view.xml',
        'views/mrp_production_view.xml',
        'views/purchase_order_view.xml',
        'views/project_edit_project.xml',
        'views/account_move_view.xml',
        'views/sale_order_search_view.xml',
        'views/view_picking_form.xml'
    ],

    'installable': True,
    'application': False,
}
