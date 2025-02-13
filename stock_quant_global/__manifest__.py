# -*- coding: utf-8 -*-
{
    'name': "Stock Quantities System Wide",

    'summary': """
        A module to show products quantities report in all companies.""",
    'author': "Ismail Mohamedi",
    'website': "http://www.yourcompany.com",

    # for the full list
    'category': 'Inventory',
    'version': '15.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['stock', 'sales_team', 'purchase'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'reports/stock_quant_template.xml',
        'reports/report_action.xml',
        'views/views.xml',
    ],

    # only loaded in demonstration mode
    'demo': [
    ],
}
