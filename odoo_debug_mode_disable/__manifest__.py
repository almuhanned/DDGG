# -*- coding: utf-8 -*-
{
    'name': "Odoo Debug Mode Disable",

    'summary': """Control Odoo backend & frontend debug modes""",

    'description': """This module gives you option to control the Odoo debug mode. You can disable it for all the users
     and allow it for the selected users. Only these selected users can use Odoo debug mode. It will be helpful in 
     increasing security and privacy of your Odoo instance.""",

    'author': "ErpMstar Solutions",
    'category': 'Tool',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/res_groups.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],

    'images': ['static/description/banner.jpg'],
    'application': True,
    'installable': True,
    'price': 11,
    'currency': 'EUR',
}
