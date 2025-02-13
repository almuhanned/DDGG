# -*- coding: utf-8 -*-

{
    'name': 'HR Payslip Report Custom',
    'version': '1.0',
    'summary': """ To custom payslip report """,
    'description': """
        To custom payslip report.
""",

    'author': 'TELENCO/Abdalrhman Ibrahim Ahmed',
    'support': 'abdalrhmanibrahim55@gmail.com',
    # 'images': ['static/description/icon.png'],
    'category': 'HR',
    'depends': ['hr_payroll'],
    'data': [

                'views/hr_work_entry_view.xml',
                'views/report_payslip_templates.xml',

    ],
    'license': 'LGPL-3',
    'demo': [],
    'installable': True,
    'application': False,
}

