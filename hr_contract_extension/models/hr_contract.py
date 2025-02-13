# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Contract(models.Model):
    _inherit = 'hr.contract'
    _description = 'Contract Extension'

    l10n_sa_housing_allowance = fields.Monetary(string='Saudi Housing Allowance')
    l10n_sa_transportation_allowance = fields.Monetary(string='Saudi Transportation Allowance')
    l10n_sa_other_allowances = fields.Monetary(string='Saudi Other Allowances')
    # number_of_days = fields.Integer(string='Saudi Number of Days',
    #                                         help='Number of days of basic salary to be added to the end of service provision per year')

    l10n_sa_company_country_code = fields.Char(related='company_country_id.code', string='Saudi Company Country Code')

    # company_country_code = fields.Char(related='company_country_id.code', string='Saudi Company Country Code')
    #
    # _sql_constraints = [
    #     ('number_of_days_constraint', 'CHECK(number_of_days >= 0)',
    #      'Number of Days must be equal to or greater than 0')
    # ]

    schedule_pay = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('semi-annually', 'Semi-annually'),
        ('annually', 'Annually'),
        ('weekly', 'Weekly'),
        ('bi-weekly', 'Bi-weekly'),
        ('bi-monthly', 'Bi-monthly'),
    ], string='Scheduled Pay', index=True, default='monthly',
    help="Defines the frequency of the wage payment.")
    struct_id = fields.Many2one('hr.payroll.structure', string='Salary Structure')
    # employee_no = fields.Char(string='Employee ID', related="employee_id.employee_no")


    def compute_allowance(self, payslip, code=None):
        result= 0.0
        for rec in payslip.contract_id.attribute_value_ids:
            if rec.attribute_id.code == code:
                result = rec.value
        return result

    def compute_deduction(self, payslip, code=None):
        result= 0.0
        for rec in payslip.contract_id.attribute_value_ids:
            if rec.attribute_id.code == code:
                result = rec.value
        return float(result)

    def get_all_structures(self):
        """
        @return: the structures linked to the given contracts, ordered by hierachy (parent=False first,
                 then first level children and so on) and without duplicata
        """
        structures = self.mapped('struct_id')
        if not structures:
            return []
        # YTI TODO return browse records
        return list(set(structures._get_parent_structure().ids))



