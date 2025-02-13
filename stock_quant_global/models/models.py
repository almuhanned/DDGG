from odoo import models, fields, api, tools


class ProductQuantityReport(models.Model):
    _name = 'product.quantity.report'
    _auto = False

    product_id = fields.Many2one('product.product', 'Product', readonly=True)
    product_uom_id = fields.Many2one('uom.uom', 'Unit of Measure', readonly=True)
    product_category_id = fields.Many2one("product.category", readonly=1)
    on_hand_qty = fields.Float('On Hand Quantity', readonly=True)
    reserved_quantity = fields.Float('Reserved Quantity', readonly=True)
    available_qty = fields.Float('Available Quantity', readonly=True)
    company_id = fields.Many2one('res.company', 'Company', readonly=True)
    location_id = fields.Many2one('stock.location', 'Location', readonly=True)
    usage = fields.Char('Usage', readonly=True)
    lot_id = fields.Many2one('stock.production.lot', 'Lot/Serial Number', readonly=True)

    def _select(self):
        return """
            SELECT
                MIN(q.id) AS id,
                p.id AS product_id,
                q.company_id AS company_id,
                q.location_id AS location_id,
                q.lot_id AS lot_id,
                l.usage AS usage,
                SUM(q.quantity) AS on_hand_qty,
                SUM(q.reserved_quantity) AS reserved_quantity,
                SUM(q.quantity - q.reserved_quantity) AS available_qty,
                pt.uom_id as product_uom_id,
                pt.categ_id as product_category_id 
        """

    def _from(self):
        return """
            FROM stock_quant AS q
                LEFT JOIN product_product p ON (q.product_id=p.id)
                LEFT JOIN product_template pt ON (p.product_tmpl_id=pt.id)
                LEFT JOIN uom_uom u ON (u.id=pt.uom_id)
                LEFT JOIN stock_location l ON (l.id=q.location_id)
                LEFT JOIN product_category c ON (c.id=pt.categ_id)
        """

    def _group_by(self):
        return """
            GROUP BY
                p.id,
                pt.uom_id,
                pt.categ_id,
                q.company_id,
                q.location_id,
                q.lot_id,
                l.usage,
                pt.categ_id
        """

    def init(self):
        tools.drop_view_if_exists(self._cr, 'product_quantity_report')
        self._cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                %s
                %s
                %s
            )
        """ % ('product_quantity_report', self._select(), self._from(), self._group_by())
                         )


class vehcile_rent_report_template(models.AbstractModel):
    _name = 'report.stock_quant_global.stock_quant_template'

    def _get_report_values(self, docids, data=None):
        # Company data
        company_name = self.env.user.company_id.name
        company_street = self.env.user.company_id.street
        company_street2 = self.env.user.company_id.street2
        company_city = self.env.user.company_id.city
        company_state = self.env.user.company_id.state_id.name
        company_phone = self.env.user.company_id.phone
        company_email = self.env.user.company_id.email
        company_vat = self.env.user.company_id.vat
        company_logo = self.env.user.company_id.logo

        # Stock quant data
        stock_quant = self.env['product.quantity.report'].browse(docids)

        return {'docs': stock_quant,
                'company_name': company_name,
                'company_street': company_street,
                'company_street2': company_street2,
                'company_city': company_city,
                'company_state': company_state,
                'company_phone': company_phone,
                'company_email': company_email,
                'company_vat': company_vat,
                'company_logo': company_logo
                }
