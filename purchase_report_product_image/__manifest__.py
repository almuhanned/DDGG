# See LICENSE file for full copyright and licensing details.

{
    # Module information
    "name": "Product Image for Purchase",
    "version": "15.0.1.0.0",
    "category": "Sales Management",
    "sequence": "1",
    "summary": """Product Image for Quatation/Purchase Reports.""",
    "description": """Product Image for Quatation/Purchase Reports.""",
    "license": "LGPL-3",
    # Author
    "author": "Serpent Consulting Services Pvt. Ltd.",
    "website": "http://www.serpentcs.com",
    "maintainer": "Serpent Consulting Services Pvt. Ltd.",
    # Dependencies
    "depends": ["purchase"],
    # Views
    "data": [
        "views/sale_product_view.xml",
        "views/report_saleorder.xml"
    ],
    # Techical
    "installable": True,
    "auto_install": False,
}
