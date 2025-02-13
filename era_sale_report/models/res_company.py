# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResCompany(models.Model):
    _inherit = 'res.company'

    ar_name = fields.Char(string="Arabic Name")

    fax = fields.Char(string="Fax")
    ar_fax = fields.Char(string="Arabic Fax")

    po_box = fields.Char(string="P.O Box")
    ar_po_box = fields.Char(string="Arabic P.O Box")

    ar_phone = fields.Char(string="Arabic Phone")
    ar_company_registry = fields.Char(string="Arabic Company Registry")

    street3 = fields.Char(string="Address 2")

    ar_address = fields.Html(string="Arabic Address")
    en_address = fields.Html(string="Address")

    ar_street2 = fields.Char(string="Arabic Address 2")
    ar_street3 = fields.Char(string="Arabic Address3")

    warranty = fields.Char(string="Warranty", translate=True)
    sales_terms = fields.Html(string="Sale Terms & Condition", translate=True)
    thanks_msg = fields.Html(string="Thanks Message", translate=True)
    best_regards = fields.Char(string="Best Regards", default='WAHAJ ALMAS', translate=True)

    terms_url = fields.Char(string="Terms URL")

    purchase_terms_title = fields.Char(string="Purchase Terms & Condition Title", translate=True)
    purchase_terms = fields.Html(string="Purchase Terms & Condition", translate=True)

    hide_arabic = fields.Boolean(string="Hide Arabic")
    invoice_ar_terms_title = fields.Char(string="Invoice Terms & Condition Title", translate=True)
    invoice_ar_terms_msg = fields.Char(string="Invoice Terms Message", translate=True)
    invoice_ar_terms_section1 = fields.Html(string="Invoice Terms & Condition #1", translate=True)
    invoice_ar_terms_section2 = fields.Html(string="Invoice Terms & Condition #2", translate=True)
    invoice_ar_terms_section3 = fields.Html(string="Invoice Terms & Condition #3", translate=True)
    invoice_ar_terms_section4 = fields.Html(string="Invoice Terms & Condition #4", translate=True)

    hide_english = fields.Boolean(string="Hide English")
    invoice_en_terms_title = fields.Char(string="Invoice Terms & Condition Title en", translate=True)
    invoice_en_terms_msg = fields.Char(string="Invoice Terms Message en", translate=True)
    invoice_en_terms_section1 = fields.Html(string="Invoice Terms & Condition #1 en", translate=True)
    invoice_en_terms_section2 = fields.Html(string="Invoice Terms & Condition #2 en", translate=True)
    invoice_en_terms_section3 = fields.Html(string="Invoice Terms & Condition #3 en", translate=True)
    invoice_en_terms_section4 = fields.Html(string="Invoice Terms & Condition #4 en", translate=True)

