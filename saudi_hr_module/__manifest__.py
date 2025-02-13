# -*- coding: utf-8 -*-

{
    'name': 'Odoo15 Employee Profile Edits',
    'version': '15.0.1.0.0',
    'category': 'Human Resources',
    'summary': """
        Employee Profile Edits
    """,
    'description': """Employee Profile Edits""",
    'author': 'Sharek Telecom & IT Redefined',
    'company': 'Sharek Telecom & IT Redefined',
    'maintainer': 'Sharek Telecom & IT Redefined',
    'website': 'https://www.sharek.com.sa',
    'depends': ['hr'],
    'data': [

        'views/hr_employee_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'AGPL-3',
}
