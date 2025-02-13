# -*- coding: utf-8 -*-

{
    'name': 'Sales Custom Module',
    'version': '15.0.1.0.0',
    'category': 'Sales',
    'summary': """
        Sales Orders Edits
    """,
    'description': """Employee Profile Edits""",
    'author': 'Sharek Telecom & IT Redefined',
    'company': 'Sharek Telecom & IT Redefined',
    'maintainer': 'Sharek Telecom & IT Redefined',
    'website': 'https://www.sharek.com.sa',
    'depends': ['sale','account', 'hr'],
    'data': [

        'views/sale_view.xml',
        'views/account_move_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'AGPL-3',
}
