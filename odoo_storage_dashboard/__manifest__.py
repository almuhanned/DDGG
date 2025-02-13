# -*- coding: utf-8 -*-

{
    'name': 'Odoo Storage Dashboard',
    'version': '15.0.0.2',
    'summary': """Displays Storage Information Of the database. Odoo Memory Usage Dashboard Screen. Postgres.""",
    'description': """Displays Storage Information Of the database.""",
    'category': 'Extra Tools',
    'author': 'bisolv',
    'website': "www.bisolv.com",
    'license': 'AGPL-3',

    'price': 35.0,
    'currency': 'USD',

    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'views/dashboard_view.xml',
    ],
    'demo': [

    ],
    'images': ['static/description/banner.png'],
    'qweb': [],

    'installable': True,
    'auto_install': False,
    'application': False,
}
