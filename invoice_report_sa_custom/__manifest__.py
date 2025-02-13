# -*- coding: utf-8 -*-
{
    'name': "Invoice Report Custom Design",

    'summary': """
        Invoice Report Custom Design""",


    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['l10n_sa_invoice','sale','purchase','stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/account_move_views.xml',
        'report/report_layout.xml',
        'report/account_invoice_report_view.xml'
    ],

    'assets': {
        
        'web.report_assets_common': [
            'invoice_report_sa_custom/static/fonts/fonts.css',
        ],
        
    } ,
    
}
