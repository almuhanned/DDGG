# -*- coding: utf-8 -*-
{
    'name': "Contract Extension (Saudi)",

    'summary': """
       Contract Extension""",

    'description': """
        Contract Extension
    """,

    'author': "",
    'website': "http://www.yourcompany.com",

    'category': 'Human Resource/Contract',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr_contract', 'hr_holidays', 'hr_payroll'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'data/hr_payroll_demo.xml',
        'views/hr_contract_view.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
