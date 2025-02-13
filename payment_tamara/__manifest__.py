# -*- coding: utf-8 -*-
##########################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
##########################################################################

{
    "name":  "Tamara Payment Connect",
    "summary":  "Tamara Payment Connect",
    "category":  "Accounting",
    "version":  "1.0.8",
    "sequence":  1,
    "author":  "Webkul Software Pvt. Ltd.",
    "license":  "Other proprietary",
    "website":  "https://store.webkul.com/odoo-tamara-payment-connect.html",
    "description":  """Tamara Payment Connect""",
    "live_test_url":'https://odoodemo.webkul.com/?module=payment_tamara&version=15.0',
    "depends":  [
        'payment','website_sale_delivery'
    ],
    "data":  [
        'views/payment_acquirer.xml',
        'views/payment_tamara_templates.xml',
        'data/tamara_payment_data.xml',
        'views/template.xml',
    ],

    "assets"    :  {
                    'web.assets_frontend': [
                            '/payment_tamara/static/src/js/product_widget.js'
                        ],
                },
    "images":  ['static/description/Banner.gif'],
    "application":  True,
    "installable":  True,
    "price":  149,
    "currency":  "USD",
    "pre_init_hook":  "pre_init_check",
    "external_dependencies":  {"python" : ["jwt"]},
}
