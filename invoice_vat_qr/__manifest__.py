# -*- coding: utf-8 -*-
# Copyright 2019, 2021 Openworx
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    "name": "E-Invoice For VAT and Zakat in KSA",
    "summary": "Add IBAN QR Code on Invoice for scanning in mobile banking apps",
    "version": "0.1",
    "author": "SNIT",
    'category': 'Accounting',
    "depends": ['base', 'account', 'sale_management','driver_in_invoice'],
    "data": [
        'views/invoice_vat_qr.xml',
        'views/person_vat_invoice.xml',
        'views/simple_invoice.xml',
        'views/res_company_view.xml',
        'reports/report_invoice.xml',
    ],

    'assets': {
        'web.report_assets_common': [
            '/invoice_vat_qr/static/src/css/report_style.scss',

        ],},
    "license": "LGPL-3",
    'images': ['images/ibanqr.png'],
    "installable": True,
    "application": False,
}
