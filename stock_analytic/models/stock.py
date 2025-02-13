# Copyright 2013 Julius Network Solutions
# Copyright 2015 Clear Corp
# Copyright 2016 OpenSynergy Indonesia
# Copyright 2017 ForgeFlow S.L.
# Copyright 2018 Hibou Corp.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.onchange('picking_id.analytic_account_id')
    def _get_default_analytic(self):
        """methode to get default analytic"""
        self.analytic_account_id = self.picking_id.analytic_account_id
        print('##########################################################', self.picking_id)
        print('##########################################################', self.picking_id.analytic_account_id)

    analytic_account_id = fields.Many2one(
        string="Analytic Account",
        comodel_name="account.analytic.account",
    )
    analytic_tag_ids = fields.Many2many("account.analytic.tag", string="Analytic Tags")

    other_account_id = fields.Many2one(
        'account.account', 'Other output Account', company_dependent=True,
        domain="[('company_id', '=', allowed_company_ids[0]), ('deprecated', '=', False)]", check_company=True,
        help="""When automated inventory valuation is enabled on a product category, this account will replacement of 
        output account with current value of the products.""", )

    def _prepare_account_move_line(
            self, qty, cost, credit_account_id, debit_account_id, description
    ):
        self.ensure_one()
        res = super(StockMove, self)._prepare_account_move_line(
            qty, cost, credit_account_id, debit_account_id, description
        )
        for line in res:
            if (
                    line[2]["account_id"]
                    != self.product_id.categ_id.property_stock_valuation_account_id.id
            ):
                # Add analytic account in debit line
                if self.analytic_account_id:
                    line[2].update({"analytic_account_id": self.analytic_account_id.id, })
                if self.other_account_id:
                    line[2].update({"account_id": self.other_account_id.id, })
                    # Add analytic tags in debit line
                if self.analytic_tag_ids:
                    line[2].update(
                        {"analytic_tag_ids": [(6, 0, self.analytic_tag_ids.ids)]}
                    )
        return res

    def _prepare_account_move_vals(self, credit_account_id, debit_account_id, journal_id, qty, description, svl_id, cost):
        self.ensure_one()

        move_lines = self._prepare_account_move_line(qty, cost, credit_account_id, debit_account_id, description)
        date = self._context.get('force_period_date', fields.Date.context_today(self))
        accounting_date = self.picking_id.scheduled_date or self.picking_id.date_done
        # if self.picking_id.date_done:
            # accounting_date = self.date_done
        return {
            'journal_id': journal_id,
            'branch_id': self.branch_id.id,
            'date': accounting_date,
            'line_ids': move_lines,
            'ref': description,
            'stock_move_id': self.id,
            'stock_valuation_layer_ids': [(6, None, [svl_id])],
            'move_type': 'entry',
        }

    @api.model
    def _prepare_merge_moves_distinct_fields(self):
        fields = super()._prepare_merge_moves_distinct_fields()
        fields.append("analytic_account_id")
        fields.append("other_account_id")
        return fields


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    analytic_account_id = fields.Many2one(related="move_id.analytic_account_id")
    other_account_id = fields.Many2one(
        'account.account', 'Other output Account', company_dependent=True,
        domain="[('company_id', '=', allowed_company_ids[0]), ('deprecated', '=', False)]", check_company=True,
        help="""When automated inventory valuation is enabled on a product category, this account will replacement of 
        output account with current value of the products.""", )
