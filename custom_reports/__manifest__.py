# -*- coding: utf-8 -*-
#################################################################################
#################################################################################

{
    'name': 'Custom Reports',
    'version': '15.0.1.0',
    'sequence': 1,
    'category': 'Accounting',
    'summary': 'Saudi Custom Reports',
    'description': """
     
     """,
    'author': '',
    'website': '',
    'depends': ['account','stock'],
    'data': [
        'report/payment_report.xml',
        'report/stock_reports.xml',
    ],
    'images': ['static/description/banner.gif'],
    'installable': True,
    'auto_install': False,
    'application': True,
}
