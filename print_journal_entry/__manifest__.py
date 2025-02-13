# -*- coding: utf-8 -*-
{
    'name': "Print Journal Entery",

    'summary': """
        Print Journal Entery""",

    'description': """
        Print Journal Entery
    """,

    'author': "Yusra Mohamed",
    'website': "http://www.noptechs.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '15.0',

    # any module necessary for this one to work correctly
    'depends': ['base','account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
