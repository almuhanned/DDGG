# -*- coding: utf-8 -*-
# Part of Probuse Consulting Service Pvt Ltd. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Total Payment Amount In Words',
    'version' : '3.1.3',
    'price' : 12.0,
    'currency': 'EUR',
    'category': 'Accounting/Accounting',
    'license': 'Other proprietary',
    'summary' : 'Payment Amount in Words for Customer and Supplier Payment',
    'description': """
Total Payment Amount In Words
    """,
    'author' : 'Probuse Consulting Service Pvt. Ltd.',
    'website' : 'www.probuse.com',
    'depends' : [
        'account',
    ],
    'support': 'contact@probuse.com',
    'images': ['static/description/img.jpg'],
    'live_test_url': 'https://probuseappdemo.com/probuse_apps/amount_word_payment_receipt/327',#'https://youtu.be/Ob2X964JZQs',
    'data' : [
        'views/account_payment_view.xml',
        'views/payment_report_template.xml',
    ],
    'qweb': [
    ],
    'installable' : True,
    'application' : False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
