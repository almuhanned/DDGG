from odoo import api, fields, models

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    location = fields.Char("location")
    contact_person = fields.Char(string="Contact Person")
    contact_phone = fields.Char(string="Phone")
    contact_email = fields.Char(string="Email")
    project_name = fields.Char(string="Project")
    validity_day = fields.Char(string="Validity Days", compute="compute_validity_day")
    delivery_data = fields.Char(string="Delivery Date", translate=True)
    commitment_day = fields.Char(string="Commitment Days", compute="compute_commitment_day")

    @api.depends("validity_date")
    def compute_validity_day(self):
        for order in self:
            date = ""
            if order.validity_date:
                diff = order.validity_date - order.create_date.date()
                date = str(diff.days)
            order.validity_day = date

    @api.depends("commitment_date")
    def compute_commitment_day(self):
        for order in self:
            days = ""
            if order.commitment_date:
                diff = order.commitment_date.date() - order.create_date.date()
                days = str(diff.days)
            order.commitment_day = days

    @api.model
    def _get_term_url(self):
        return self.env.company.terms_url
