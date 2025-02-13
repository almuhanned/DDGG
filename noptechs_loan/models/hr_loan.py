# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError
# from dateutil import relativedelta
import math

class LoansType(models.Model):
    _name = "hr.loan.type"
    _description = "Loans Types"

    name = fields.Char(string='Loan Name', required=True, translate=True)
    code = fields.Char(string='Loan code')
    active = fields.Boolean(default=True)
    start_date = fields.Date('Start Date', default=fields.Date.context_today)
    end_date = fields.Date('End Date')
    loan_type = fields.Selection([
        ('fixed','Fixed Amount'),
        ('salary','Based on Salary')
    ], required=True, default='fixed', string='Loan Type')
    loan_amount = fields.Float(string="Loan Amount", required=True)
    max_loan_amount = fields.Float(string="Max Loan Amount")
    factor = fields.Float(string="Factor", default=1 )
    installment = fields.Integer(string="No Of Installments",required=True, default=1)
    loan_account_id = fields.Many2one('account.account', domain=[('deprecated', '=', False)], string="Loan Account")
    loan_journal_id = fields.Many2one('account.journal','Journal')
    payment_journal_id = fields.Many2one('account.journal','Payment Journal')
    times_stop_loan =fields.Integer(string="Times of Stop Loan")
    period_stop_loan = fields.Integer(string="Period of Stop Loan")
    loan_limit = fields.Selection([
        ('one','Once'),
        ('unlimit','Unlimit')], default='one', string='Limit', required=True)
    salary_rule_ids = fields.Many2many('hr.salary.rule', string='Salary Rules')
    level_ids = fields.Many2many('hr.payroll.structure',  string='Levels')
    interference = fields.Boolean(string='Allow Interference')
    guarantor = fields.Boolean(string="Need Guarantor")
    year_employment =fields.Integer(string="Years of Employment")
    validation = fields.Boolean(string="Apply Double Validation ")
    note = fields.Text(string='Description')
    decimal_calculate = fields.Selection([
        ('with','With decimal part'),
        ('without','Without decimal part')], default='with', string='decimal calculating', required=True)
    # salary_struct_id = fields.Many2many('hr.payroll.structure')

    # employee_account_id = fields.Many2one('account.account', string="Loan Account", required=True)
    # treasury_account_id = fields.Many2one('account.account', string="Treasury Account", required=True)
    # journal_id = fields.Many2one('account.journal', string="Journal", required=True)

    _sql_constraints = [
        ('code_uniq', 'unique (code)', 'The code of the loan must be unique !'),
        ('name_uniqe', 'unique (name)', 'The name of the loan must be unique !'),
    ]

class InstallmentLine(models.Model):
    _name = "hr.loan.line"
    _description = "Installment Line"

    date = fields.Date(string="Payment Date", required=True, help="Date of the payment")
    employee_id = fields.Many2one('hr.employee', string="Employee", help="Employee")
    amount = fields.Float(string="Amount", required=True, help="Amount")
    paid = fields.Boolean(string="Paid", help="Paid")
    loan_id = fields.Many2one('hr.loan', string="Loan Ref.", help="Loan")
    payslip_id = fields.Many2one('hr.payslip', string="Payslip Ref.", help="Payslip")


class HrLoan(models.Model):
    _name = 'hr.loan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Loan Request"

    @api.model
    def default_get(self, field_list):
        result = super(HrLoan, self).default_get(field_list)
        if result.get('user_id'):
            ts_user_id = result['user_id']
        else:
            ts_user_id = self.env.context.get('user_id', self.env.user.id)
        result['employee_id'] = self.env['hr.employee'].search([('user_id', '=', ts_user_id)], limit=1).id
        return result

    def _compute_loan_amount(self):
        total_paid = 0.0
        for loan in self:
            for line in loan.loan_lines:
                if line.paid:
                    total_paid += line.amount
            balance_amount = loan.loan_amount - total_paid
            loan.total_amount = loan.loan_amount
            loan.balance_amount = balance_amount
            loan.total_paid_amount = total_paid

    loan_type_id = fields.Many2one('hr.loan.type', string='Loan Type', required=True,)
    name = fields.Char(string="Loan Name", default="/", readonly=True, help="Name of the loan")
    date = fields.Date(string="Date", default=fields.Date.today(), readonly=False, help="Date")
    employee_id = fields.Many2one('hr.employee', string="Employee", required=True, help="Employee", store="True")
    department_id = fields.Many2one('hr.department', related="employee_id.department_id", readonly=True,
                                    string="Department", store="True", help="Employee")
    installment = fields.Integer(string="No Of Installments", default=1, help="Number of installments")
    payment_date = fields.Date(string="Payment Start Date", required=True, default=fields.Date.today(), help="Date of "
                                                                                                             "the "
                                                                                                             "paymemt")
    loan_lines = fields.One2many('hr.loan.line', 'loan_id', string="Loan Line", index=True)
    company_id = fields.Many2one('res.company', 'Company', readonly=True, help="Company",
                                 default=lambda self: self.env.user.company_id,
                                 states={'draft': [('readonly', False)]})
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, help="Currency",
                                  default=lambda self: self.env.user.company_id.currency_id)
    job_position = fields.Many2one('hr.job', related="employee_id.job_id", readonly=True, string="Job Position",
                                   help="Job position")
    loan_amount = fields.Float(string="Loan Amount", required=True, help="Loan amount")
    total_amount = fields.Float(string="Total Amount", store=True, readonly=True, compute='_compute_loan_amount',
                                help="Total loan amount")
    balance_amount = fields.Float(string="Balance Amount", store=True, compute='_compute_loan_amount', help="Balance amount")
    total_paid_amount = fields.Float(string="Total Paid Amount", store=True, compute='_compute_loan_amount',
                                     help="Total paid amount")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting_approval_1', 'Submitted'),
        ('approve', 'Approved'),
        ('refuse', 'Refused'),
        ('cancel', 'Canceled'),
    ], string="State", default='draft', track_visibility='onchange', copy=False, )
    type_loan = fields.Char()

    @api.onchange('loan_amount')
    def onchange_loan_amount(self):
        if self.loan_type_id and self.loan_type_id.loan_type == 'salary':
            if self.loan_amount >= self.loan_type_id.max_loan_amount:
                self.loan_amount = self.loan_type_id.max_loan_amount
                raise ValidationError(_("The loan amount should be less than or equal max loan amount"))

    @api.model
    def create(self, values):
        loan_count = self.env['hr.loan'].search_count(
            [('employee_id', '=', values['employee_id']), ('state', '=', 'approve'),
             ('balance_amount', '!=', 0)])
        if loan_count:
            raise ValidationError(_("The employee has already a pending installment"))
        else:
            values['name'] = self.env['ir.sequence'].get('hr.loan.seq') or ' '
            res = super(HrLoan, self).create(values)
            return res

    @api.depends('loan_type_id','loan_amount','installment')
    def compute_installment(self):
        """This automatically create the installment the employee need to pay to
        company based on payment start date and the no of installments.
            """
        for loan in self:
            loan.loan_lines.sudo().unlink()
            date_start = datetime.strptime(str(loan.payment_date), '%Y-%m-%d')
            amount = loan.loan_amount / loan.installment
            for i in range(1, loan.installment + 1):
                self.env['hr.loan.line'].create({
                    'date': date_start,
                    'amount': amount,
                    'employee_id': loan.employee_id.id,
                    'loan_id': loan.id})
                date_start = date_start + relativedelta(months=1)
            loan._compute_loan_amount()
        return True

    @api.onchange('loan_type_id')
    def _onchange_loan_type_id(self):
        if self.loan_type_id.loan_type == 'fixed':
            self.loan_amount = self.loan_type_id.loan_amount
            self.installment = self.loan_type_id.installment
            self.type_loan = 'fixed'
        if self.loan_type_id.loan_type == 'salary':
            self.loan_amount = 0.0
            self.installment = 1
            self.type_loan = 'salary'

    def action_refuse(self):
        return self.write({'state': 'refuse'})

    def action_submit(self):
        level = self.env['hr.payroll.structure'].search([]).ids
        emp_structure = self.env['hr.contract'].search([('employee_id','=',self.employee_id.id),('state','=','open')])
        if self.loan_type_id.level_ids:
             level = self.loan_type_id.level_ids.ids
        if self.employee_id and emp_structure.structure_type_id.default_struct_id.id in level:

            self.write({'state': 'waiting_approval_1'})
        else:  
             self.write({'state': 'waiting_approval_1'})

    def action_cancel(self):
        self.write({'state': 'cancel'})

    def action_approve(self):

        for data in self:
            if not data.loan_lines:
                raise ValidationError(_("Please Compute installment"))
            else:
                self.write({'state': 'approve'})

    def unlink(self):
        for loan in self:
            if loan.state not in ('draft', 'cancel'):
                raise UserError(
                    'You cannot delete a loan which is not in draft or cancelled state')
        return super(HrLoan, self).unlink()



class HrEmployee(models.Model):
    _inherit = "hr.employee"

    def _compute_employee_loans(self):
        """This compute the loan amount and total loans count of an employee.
            """
        self.loan_count = self.env['hr.loan'].search_count([('employee_id', '=', self.id)])

    loan_count = fields.Integer(string="Loan Count", compute='_compute_employee_loans')
