# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta, time, datetime
from dateutil.relativedelta import relativedelta
# import datetime


class EndOfServiceAward(models.Model):
    _inherit = 'end.of.service.award'

    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id, string='Currency', readonly=True)
    holiday_days = fields.Float(compute='_compute_holiday_days',  string="Leave amount due", tracking=True)#override field
    number_of_days_from_rejoin_date = fields.Float(compute='_compute_number_of_days_from_rejoin_date', string='Number Of Days from Rejoin Date')
    number_of_days_from_rejoin_date_text = fields.Char(compute='_compute_number_of_days_from_rejoin_date', string='Number Of Days from Rejoin Date')
    duration_days = fields.Float(compute='_compute_duration_days', string="number of Leave day due ")
    duration_days_text = fields.Char(compute='_compute_duration_days')
    other_amount = fields.Float(string='Other Amount')
    other_ded_amount = fields.Float(string='Other deduction')
    loan_amount = fields.Float('Loan Amount', compute='compute_loan_amount')
    total = fields.Float(compute='_compute_total_remaining_duration')
    total_amount = fields.Float(string='Total Amount', compute="compute_total_amount")
    eos_note = fields.Char(string='Note')
    
    account_holiday_id = fields.Many2one(
        string='Account Holiday',
        comodel_name='account.account',
        required=True
    )
    account_end_service_id = fields.Many2one(
        string='Salary',
        comodel_name='account.account',
        required=True
    )
    account_id = fields.Many2one(
        string='Account',
        comodel_name='account.account',
        required=True
    )
    journal_id = fields.Many2one(
        string='Journal',
        comodel_name='account.journal',
        required=True
    )
    account_move_id = fields.Many2one(
        string='Account Move',
        comodel_name='account.move',
    )

    account_other_allownces_id = fields.Many2one(
        string='Other Allownces',
        comodel_name='account.account',
        required=True
    )

    account_other_deduction_id = fields.Many2one(
        string='Other Deduction',
        comodel_name='account.account',
        required=True
    )

    account_move_state = fields.Char(compute="get_account_move_state", store=True)

    loan_account_id = fields.Many2one('account.account', string="Loan Account", default=lambda self: self.env['employee.loan.type']\
        .search([], limit=1).loan_account)
    last_work_date = fields.Date(tracking=True)
    request_date = fields.Date(string="Request Date", default=fields.Date.today)


    
    
    @api.depends('remaining_amount', 'loan_amount', 'holiday_days', 'other_amount', 'other_ded_amount')
    def compute_total_amount(self):
        for rec in self:
            rec.total_amount = rec.remaining_amount + rec.other_amount - rec.loan_amount - rec.other_ded_amount + rec.holiday_days 
    @api.depends('employee_id')
    def compute_loan_amount(self):
        for rec in self:
            installment_ids = self.env['installment.line'].search(
                [('employee_id', '=', rec.employee_id.id), ('loan_id.state', '=', 'done'),
                 ('is_paid', '=', False)])
            rec.loan_amount = sum(installment_ids.mapped('total_installment'))

    @api.depends('employee_id', 'last_work_date')    
    def _compute_duration_days(self):
        company = self.env['res.company'].search([('id', '=', self.env.user.company_id.id)])
        leave_type_id = company.leave_type_id
        if leave_type_id:
            hr_leave_allocation = self.env['hr.leave.allocation'].sudo()\
                .search([('employee_id.id', '=', self.employee_id.id),
                         ('state', '=', 'validate'),
                         ('holiday_status_id.id', '=', leave_type_id.id)])
            hr_leave = self.env['hr.leave'].sudo()\
                .search([('employee_id.id', '=', self.employee_id.id),
                         ('state', '=', 'validate'),
                         ('holiday_status_id.id', '=', leave_type_id.id)])
            total_days = total_leave_days = 0.0
            today = datetime.combine(fields.Date.today(), time(0, 0, 0))
            last_work_date = datetime.combine(self.last_work_date, time(0, 0, 0))
            this_year_first_day = today + relativedelta(day=1, month=1)
            end_of_year_allocations = self.env['hr.leave.allocation'].search(
            [('allocation_type', '=', 'accrual'), ('state', '=', 'validate'), ('accrual_plan_id', '!=', False), ('employee_id', '=', self.employee_id.id),
                '|', ('date_to', '=', False), ('date_to', '>', fields.Datetime.now()), ('lastcall', '<', this_year_first_day), ('holiday_status_id.id', '=', leave_type_id.id)])
            end_of_year_allocations._end_of_year_accrual()
            end_of_year_allocations.flush()
            allocations = self.env['hr.leave.allocation'].search(
            [('allocation_type', '=', 'accrual'), ('state', '=', 'validate'), ('accrual_plan_id', '!=', False), ('employee_id', '=', self.employee_id.id),
                '|', ('date_to', '=', False), ('date_to', '>=', last_work_date), ('holiday_status_id.id', '=', leave_type_id.id)
             ])
            leaves = allocations.mod_process_accrual_plans(self.last_work_date, allocations)

            if hr_leave_allocation:
                total_days = sum([allocate.number_of_days_display for allocate in hr_leave_allocation])
                total_leave_days = sum([leave.number_of_days for leave in hr_leave])
            if total_days > 0.0:
                if leaves and leaves > 0:
                    self.duration_days = leaves - sum(allocations.mapped('leaves_taken'))
                else:
                    self.duration_days = total_days - total_leave_days
                self.duration_days_text = "%d Years, %d Months, %d Days" %(int(self.duration_days / 360), int((self.duration_days % 360) / 30), int(((self.duration_days % 360) % 30)))
            else:
                self.duration_days = 0.0
                self.duration_days_text = "0 Years, 0 Months, 0 Days"
        else:
            self.duration_days = 0.0
            self.duration_days_text = "0 Years, 0 Months, 0 Days"

    @api.depends('amount_received', 'final_deserving')
    def _compute_remaining_amount(self):
        for rec in self:
            total = rec.final_deserving - rec.amount_received
            if total < 0 :
                rec.remaining_amount = 0.0
            else:
                rec.remaining_amount = total
    
    @api.depends('remaining_amount', 'holiday_days')
    def _compute_total_remaining_duration(self):
        for rec in self:
            rec.total = rec.remaining_amount + rec.holiday_days
            # rec.total_amount = rec.total
    
    # @api.onchange('other_amount')
    # def _onchange_other_amount(self):
    #     for rec in self:
    #         rec.total_amount += rec.other_amount
    
    # @api.onchange('other_ded_amount')
    # def _onchange_other_deduct_amount(self):
    #     for rec in self:
    #         rec.total_amount -= rec.other_ded_amount
    
    # @api.onchange('loan_amount')
    # def _onchange_loan_amount(self):
    #     for rec in self:
    #         rec.total_amount -= rec.loan_amount
    
    @api.depends('account_move_id.state')
    def get_account_move_state(self):
        for rec in self:
            if rec.account_move_id:
                rec.account_move_state = rec.account_move_id.state
            else:
                rec.account_move_state = ''

    @api.depends('request_date', 'last_work_date')
    def _compute_number_of_days_from_rejoin_date(self):
        for rec in self:
            rec.number_of_days_from_rejoin_date = 0
            rec.number_of_days_from_rejoin_date_text = "0 Years, 0 Months, 0 Days"
            if rec.last_work_date and rec.rejoin_date:
                days = relativedelta(rec.last_work_date + timedelta(days=1), rec.rejoin_date).days
                months = relativedelta(rec.last_work_date + timedelta(days=1), rec.rejoin_date).months
                years = relativedelta(rec.last_work_date + timedelta(days=1), rec.rejoin_date).years
                rec.number_of_days_from_rejoin_date_text = "%d Years, %d Months, %d Days" %(years, months, days)
                number_of_days_rejoin_date = rec.last_work_date - rec.request_date
                if rec.contract_id.no_of_days_leave == "no_30":        
                    rec.number_of_days_from_rejoin_date = number_of_days_rejoin_date.days * 0.0822
                else:
                    rec.number_of_days_from_rejoin_date = number_of_days_rejoin_date.days * 0.0616
    
    def _compute_holiday_days(self):
        res = super(EndOfServiceAward, self)._compute_holiday_days()
        for rec in self:
            if rec.last_work_date:
                rec.holiday_days = ((rec.contract_id.wage + rec.contract_id.home_allowance + rec.contract_id.transportation_allowance) / 30) * \
                                                                                                 ( round(rec.duration_days, 2))
            else:
                rec.holiday_days = 0
        return res
   
    def action_approve(self):
        self.get_employee_end_of_service(self.employee_id, self.last_work_date, self.contact_end_type)
        self.action_journal_enteries()
        self.state = "approved"
    
    def action_draft(self):
        for rec in self:
            rec.account_move_id.unlink()
            rec.state = 'draft'
            rec.has_custody = True
    

    def action_journal_enteries(self):
        for rec in self:
            line_ids = []
            move = {
                'name': '/',
                'journal_id': rec.journal_id.id,
                'date': rec.last_work_date,
                # 'ref': rec.employee_code,
                'move_type':'entry',
            }
            if rec.other_amount==0:
                debit3=0.0
            if rec.other_ded_amount==0:
                credit1=0.0
                
            debit1 = rec.holiday_days
            debit2 = rec.remaining_amount
            debit3 = rec.other_amount
            credit1= rec.other_ded_amount
            credit = debit1 + debit2 +debit3 -credit1

            partner_id = self.employee_id.address_home_id.id

            if rec.holiday_days <= 0:
                line_ids +=[(0,0,{
                    'account_id': rec.account_end_service_id.id,
                    'name': 'End Service Amount',
                    'partner_id': partner_id,
                    'debit':debit2,
                }), 
                (0,0,{
                    'account_id': rec.account_id.id,
                    'name': 'Main account',
                    'partner_id': partner_id,
                    'credit': credit,
                    })
                ]
            else:
                line_ids +=[(0,0,{
                    'account_id': rec.account_holiday_id.id,
                    'name': 'Holiday Amount',
                    'partner_id': partner_id,
                    'debit':debit1,

                }), (0,0,{
                    'account_id': rec.account_end_service_id.id,
                    'name': 'End Service Amount',
                    'partner_id': partner_id,
                    'debit':debit2,
                }), 
                (0,0,{
                    'account_id': rec.account_id.id,
                    'name': 'Main account',
                    'partner_id': partner_id,
                    'credit': credit,
                    })
                ]
            if rec.loan_amount > 0:
                salary_account = self.env['hr.salary.rule'].search([('code', '=', 'NET')], limit=1).account_credit
                if not salary_account:
                    raise ValidationError("Please set a credit account on 'NET' salary rules!")
                line_ids += [
                    (0, 0, {
                        'account_id': rec.loan_account_id.id,
                        'name': 'Loan',
                        'partner_id': partner_id,
                        'debit': rec.loan_amount,
                    }),
                    (0, 0, {
                        'account_id': salary_account.id,
                        'partner_id': partner_id,
                        'credit': rec.loan_amount,
                    })
                ]
                installment_ids = self.env['installment.line'].search(
                [('employee_id', '=', rec.employee_id.id), ('loan_id.state', '=', 'done'),
                 ('is_paid', '=', False)])
                installment_ids.update({'is_paid': True})

            if line_ids:
                move.update({'line_ids':line_ids})
                move_context = self.env['account.move'].with_context(check_move_validity=False)
                move_id = move_context.create(move)
                rec.account_move_id = move_id.id
            return True

