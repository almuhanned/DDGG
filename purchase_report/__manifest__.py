# See LICENSE file for full copyright and licensing details.

{
    # Module information
    "name": "Purchase Report",
    "version": "15.0.1.0.0",
    "category": "Purchase",
    "sequence": "1",
    "summary": """""",
    "description": """""",
    "license": "LGPL-3",
    # Author
    "author": "",
    "website": "",
    "maintainer": "",
    # Dependencies
    "depends": ["purchase",'sale'],
    # Views
    "data": [
        "views/purchase_view.xml",
        "views/vendor_view.xml",
        "report/report_purchaseorder.xml"
    ],
    # Techical
    "installable": True,
    "auto_install": False,
}
