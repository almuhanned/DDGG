# -*- coding: utf-8 -*-

{
    'name': 'HR Leave Calendar Days',
    'version': '1.0',
    'summary': """ To remove weekend from leave """,
    'description': """
        To remove weekend from leave.
""",

    'author': 'TELENCO/Abdalrhman Ibrahim Ahmed',
    'support': 'abdalrhmanibrahim55@gmail.com',
    # 'images': ['static/description/icon.png'],
    'category': 'HR',
    'depends': ['hr_holidays'],
    'data': [

                'views/hr_leave_type_view.xml'
    ],
    'license': 'LGPL-3',
    'demo': [],
    'installable': True,
    'application': False,
}

