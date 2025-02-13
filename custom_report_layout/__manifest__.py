# -*- coding: utf-8 -*-
{
    'name': "Custom Report Layout",
    'version': '15.0.1.0.0',
    'summary': 'A module to configure report header and footer',
    'sequence': -100,
    'description': 'A module to configure report header and footer manually from company form',
    'author': "Ismail Mohamedi",
    'website': "https://www.linkedin.com/in/ismail-mohamedi-605537179",
    'category': 'All',
    'license': 'LGPL-3',
    'depends': ['base', 'sale', 'sale_order_line_sequence','purchase','l10n_gcc_invoice'],
    'data': [
        'report/base_document_layout.xml',
        'report/purchase_report.xml',
        'views/views.xml',
    ],
    'images': ['static/description/header_footer.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
