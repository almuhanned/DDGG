# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'K.S.A - Invoice Sharek',
    'version': '1.0.0',
    'author': 'Odoo S.A.',
    'category': 'Accounting/Localizations',
    'license': 'LGPL-3',
    'description': """
    Invoices for the Kingdom of Saudi Arabia
""",
    'depends': ['l10n_sa','web', 'l10n_gcc_invoice'],
    'data': [
        'views/report_invoice.xml',
    ],
}
