# -*- coding: utf-8 -*-
{
    'name': "ERA Sale Report",
    'summary': """Sale and Purchase Report""",
    'description': """Sale and Purchase Report""",
    'author': "ERA | Ahmed Eid",
    'website': "http://www.era.net.sa",
    'category': 'Sale',
    'version': '15.0.0.1',
    'depends': ['base', 'sale', 'product_brand_sale', 'sale_report_custom', 'sales_report_product_image',
                'sale_custom_module', 'web_digital_sign', 'purchase_report', 'account', 'l10n_sa_invoice'],
    'data': [
        'security/group_security.xml',
        'security/ir.model.access.csv',
        'views/product.xml',
        'views/sale_order.xml',
        'views/account_move.xml',
        'views/res_company.xml',
        'views/purchase_order.xml',
        'report/sale_document_report.xml',
        'report/purchase_document_report.xml',
        'report/invoice_document_report.xml',
        'report/sale_report.xml',
        'report/simple_invoice_document_report.xml'
    ],
    'assets': {
        'web.report_assets_common': [
            'era_sale_report/static/src/css/style.css',
        ],
    },
    "license": "LGPL-3",
}
