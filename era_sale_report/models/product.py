from odoo import api, fields, models

class ProductProduct(models.Model):
    _inherit = 'product.product'

    manufacture_company_id = fields.Many2one(comodel_name="res.partner", string="Manufacture Company")
    made_in = fields.Char(string="Made In")
    voltage = fields.Char(string="Voltage")
    dimensions = fields.Char(string="Dimensions")


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    manufacture_company_id = fields.Many2one(comodel_name="res.partner", string="Manufacture Company")
    made_in = fields.Char(string="Made In", compute='_compute_made_in', inverse='_set_made_in', store=True)
    voltage = fields.Char(string="Voltage", compute='_compute_voltage', inverse='_set_voltage', store=True)
    dimensions = fields.Char(string="Dimensions", compute='_compute_dimensions', inverse='_set_dimensions', store=True)

    @api.depends('product_variant_ids', 'product_variant_ids.made_in')
    def _compute_made_in(self):
        unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
        for template in unique_variants:
            template.made_in = template.product_variant_ids.made_in
        for template in (self - unique_variants):
            template.made_in = False

    def _set_made_in(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.made_in = template.made_in

    @api.depends('product_variant_ids', 'product_variant_ids.voltage')
    def _compute_voltage(self):
        unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
        for template in unique_variants:
            template.voltage = template.product_variant_ids.voltage
        for template in (self - unique_variants):
            template.voltage = False

    def _set_voltage(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.voltage = template.voltage

    @api.depends('product_variant_ids', 'product_variant_ids.dimensions')
    def _compute_dimensions(self):
        unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
        for template in unique_variants:
            template.dimensions = template.product_variant_ids.dimensions
        for template in (self - unique_variants):
            template.dimensions = False

    def _set_dimensions(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.dimensions = template.dimensions
