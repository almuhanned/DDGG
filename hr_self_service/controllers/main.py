# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import werkzeug
from odoo import http
from odoo.http import request, route
from datetime import datetime
from odoo import models, fields, _

from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.exceptions import UserError, Warning


class HrSelfService(CustomerPortal):

    @route(['/my', '/my/home'], type='http', auth="public", website=True)
    def home(self, **kw):
        values = self._prepare_portal_layout_values()
        user = request.env.user
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', user.id)])
        is_employee = 0
        if employee:
            is_employee = 1
        values['is_employee'] = is_employee
        return request.render("hr_self_service.portal_my_home_noptech", values)

    @route(['/hr/self/service'], type='http', auth="user", website=True)
    def hr_self_service(self, **kwargs):
        user = request.env.user
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', user.id)])
        if not employee:
            return request.render("hr_self_service.not_employee_template")

        time_off = len(request.env['hr.leave'].sudo().search(
            [('employee_id', '=', employee.id)]))
        tasks = request.env['project.task'].sudo().search([('user_ids', '=', user.id)])
        expenses = request.env['hr.expense'].sudo().search(
            [('employee_id', '=', employee.id)])
        advanced_salary = request.env['salary.advance'].sudo().search(
            [('employee_id', '=', employee.id)])
        leave_allocation = request.env['hr.leave.allocation'].sudo().search(
            [('employee_id', '=', employee.id)])
        # appraisal = request.env['hr.appraisal'].sudo().search([('employee_id','=',employee.id),('date_close', '>=', datetime.now().date())])
        # advanced_salary_amount = sum (m.advance for m in advanced_salary)
        payslips = request.env['hr.payslip'].sudo().search(
            [('employee_id', '=', employee.id)])
        # loans = request.env['hr.loan'].sudo().search(
        #     [('employee_id', '=', employee.id)])

        projects = []
        for task in tasks:
            if task.project_id not in projects:
                projects.append(task.project_id)

        announcement_ids_general = request.env['hr.announcement'].sudo().search([('is_announcement', '=', True),
                                                                                 ('state', 'in',
                                                                                  ('approved', 'done')),
                                                                                 ('date_start', '<=', datetime.now().date())])
        announcement_ids_emp = request.env['hr.announcement'].sudo().search([('employee_ids', 'in', employee.id),
                                                                             ('state', 'in',
                                                                              ('approved', 'done')),
                                                                             ('date_start', '<=', datetime.now().date())])
        announcement_ids_dep = request.env['hr.announcement'].sudo().search([('department_ids', 'in', employee.department_id.id),
                                                                             ('state', 'in',
                                                                              ('approved', 'done')),
                                                                             ('date_start', '<=', datetime.now().date())])
        announcement_ids_job = request.env['hr.announcement'].sudo().search([('position_ids', 'in', employee.job_id.id),
                                                                             ('state', 'in',
                                                                              ('approved', 'done')),
                                                                             ('date_start', '<=', datetime.now().date())])

        announcement_ids = announcement_ids_general + \
            announcement_ids_emp + announcement_ids_dep + announcement_ids_job

        render_values = {
            'employee': employee,
            'partner': user,
            'time_off': time_off,
            'tasks': tasks,
            'projects': projects,
            'expenses': expenses,
            'leave_allocation': leave_allocation,
            'announcement_ids': announcement_ids,
            'advanced_salary': advanced_salary,
            'payslips': payslips,
            # 'loans': loans,
        }

        return request.render("hr_self_service.my_account", render_values)

    # @route(['/web/action/open/<int:model_index>'], type='http', auth="user", website=True)
    # def web_action_open(self,model_index, **kwargs):

    #     models = [['hr.leave','tree,form,calendar,kanban,activity'],['project.project','kanban,form'],
    #             ['hr.expense','tree,kanban,form,graph,pivot,activity'],['salary.advance','tree,form'],
    #             ['hr.leave.allocation','tree,kanban,form,activity'],
    #             ['hr.appraisal','kanban,tree,form'],['hr.loan','tree,form'],
    #             ['hr.payslip','tree,kanban,form'],['hr.contract','kanban,tree,form,activity'],
    #             ['project.project','kanban,form']]

    #     model = models[model_index]

    #     partner = request.env.user.partner_id
    #     action = request.env['ir.actions.act_window'].sudo().search([('res_model','=',model[0]),('view_mode','=',model[1])])
    #     redirect_url = "/web#action=" + str(action[0].id)
    #     return request.redirect(redirect_url)

    @http.route(['/my/contracts'], type='http', auth="user", website=True)
    def portal_my_contracts(self, **kw):
        values = self._prepare_portal_layout_values()
        user_id = request.env.user.id
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', user_id)])
        contracts = employee.contract_ids

        values.update({
            'contracts': contracts,
            'page_name': 'contract',
            'default_url': '/my/contracts',
        })
        return request.render("hr_self_service.portal_my_contracts", values)

    # @http.route(['/my/appraisals'], type='http', auth="user",method='post', website=True)
    # def portal_my_appraisals(self,**kw):
    #     values = self._prepare_portal_layout_values()
    #     user_id = request.env.user.id
    #     employee = request.env['hr.employee'].sudo().search([('user_id','=',user_id)])
    #     appraisals = request.env['hr.appraisal'].sudo().search([('employee_id','=',employee.id),('date_close', '>=', datetime.now().date())])
    #
    #     values.update({
    #         'appraisals': appraisals,
    #         'page_name': 'appraisals',
    #         'default_url': '/my/appraisals',
    #     })
    #     return request.render("hr_self_service.portal_my_appraisals", values)

    @http.route(['/my/expenses'], type='json', auth="user", method='post', website=True)
    def portal_my_expenses(self, **post):
        values = self._prepare_portal_layout_values()
        user_id = request.env.user.id
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', user_id)])
        expenses = request.env['hr.expense'].sudo().search(
            [('employee_id', '=', employee.id)])
        products = request.env['product.product'].sudo().search(
            [('can_be_expensed', '=', True)])
        error = {}
        if 'submit' in post:
            if post.get('unit_amount'):
                unit_amount = post['unit_amount'].strip()
                unit_amounts = unit_amount.split('.')
                for test_unit_amount in unit_amounts:
                    if not test_unit_amount.isnumeric():
                        raise UserError(_('Unit price should be float only.'))
                        # error["unit_amount"] = _('Unit price should be float only.')

            if post.get('quantity'):
                quantity = post['quantity'].strip()
                quantitys = quantity.split('.')
                for test_quantity in quantitys:
                    if not test_quantity.isnumeric():
                        raise UserError(_('Quantity should be numbers only.'))
                        # error["quantity"] = _('Quantity should be numbers only.')

            if post.get('name'):
                name = post['name'].strip()
                names = name.split('.')
                for test_name in names:
                    if not test_name.isalnum():
                        # raise UserError(_('name should be characters or numbers only.'))
                        error["name"] = _('name should be characters or numbers only.')

            product_options = []
            for option in products:
                product_options.append(_(option.id))
            if post.get('product'):
                product = post['product'].strip()
                if product not in product_options:
                    raise UserError(_('Please choose a valid product.'))
                    # error["product"] = _('Please choose a valid product')
            if error:
                return error

            else:
                try:
                    expense_id = request.env['hr.expense'].sudo().create({
                        'name': name,
                        'product_id': int(product),
                        'quantity': quantity,
                        'unit_amount': unit_amount,
                    })
                except:
                    raise UserError(_('Set Correct  information'))
                return request.redirect('/my/expenses')

        values.update({
            'page_name': 'expenses',
            'error': error,
            'products': products,
            'expenses': expenses,
            'page_name': 'expenses',
            'default_url': '/my/expenses',
        })
        return request.render("hr_self_service.portal_my_expenses", values)

    @http.route(['/my/payslips'], type='http', auth="user", website=True)
    def portal_my_payslips(self, **post):
        values = self._prepare_portal_layout_values()
        user_id = request.env.user.id
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', user_id)])
        payslips = request.env['hr.payslip'].sudo().search(
            [('employee_id', '=', employee.id)])

        error = []
        if 'submit' in post:
            if error:
                pass

            else:
                try:
                    payslip_id = request.env['hr.payslip'].sudo().create({
                        'date_from': post['date_from'],
                        'date_to': post['date_to'],
                        'employee_id': employee.id
                    })
                except:
                    raise UserError(_('Set Correct  information'))
                return request.redirect('/my/payslips')
        values.update({
            'page_name': 'payslips',
            'payslips': payslips,
            'page_name': 'payslips',
            'default_url': '/my/payslips',
        })
        return request.render("hr_self_service.portal_my_payslips", values)

    # @http.route(['/my/loans'], type='http', auth="user", website=True)
    # def portal_my_loans(self, **post):
    #     values = self._prepare_portal_layout_values()
    #     user_id = request.env.user.id
    #     employee = request.env['hr.employee'].sudo().search([('user_id', '=', user_id)])
    #     loans = request.env['hr.loan'].sudo().search(
    #         [('employee_id', '=', employee.id)])
    #     loan_types = request.env['hr.loan.type'].sudo().search([])
    #
    #     error = []
    #     if 'submit' in post:
    #         if error:
    #             pass
    #
    #         else:
    #             try:
    #                 loan_id = request.env['hr.loan'].sudo().create({
    #                     'loan_type_id': int(post['loan_type_id']),
    #                     'loan_amount': post['amount'],
    #                     'installment': post['installment'],
    #                     'payment_date': post['date'],
    #                     'employee_id': employee.id
    #                 })
    #             except:
    #                 raise UserError(_('Set Correct  information'))
    #             return request.redirect('/my/loans')
    #
    #     values.update({
    #         'page_name': 'loans',
    #         'loan_types': loan_types,
    #         'loans': loans,
    #         'page_name': 'loans',
    #         'default_url': '/my/loans',
    #     })
    #     return request.render("hr_self_service.portal_my_loans", values)

    @http.route(['/my/advanced_salary'], type='http', auth="user", method='post', website=True)
    def portal_my_advanced_salary(self, **post):
        values = self._prepare_portal_layout_values()
        user_id = request.env.user.id
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', user_id)])
        advanced_salary = request.env['salary.advance'].sudo().search(
            [('employee_id', '=', employee.id)])
        error = []
        if 'submit' in post:
            if post.get('amount'):
                amount = post['amount'].strip()
                amounts = amount.split('.')
                for test_amount in amounts:
                    if not test_amount.isnumeric():
                        error["amount"] = _('Amount should be numbers only.')

            if post.get('reason'):
                reason = post['reason'].strip()
                reasons = reason.split('.')
                for test_reason in reasons:
                    if not test_reason.isalnum():
                        error["reason"] = _(
                            'Reason should be characters or numbers only.')

            if error:
                pass

            else:
                try:
                    advanced_salary_id = request.env['salary.advance'].sudo().create({
                        'advance': amount,
                        'reason': reason,
                        'date': post['date'],
                        'employee_id': employee.id
                    })
                except:
                    raise UserError(_('Set Correct  information'))
                return request.redirect('/my/advanced_salary')
        values.update({
            'page_name': 'advanced_salary',
            'advanced_salary': advanced_salary,
            'page_name': 'advanced salary',
            'default_url': '/my/advanced_salary',
        })
        return request.render("hr_self_service.portal_my_advanced_salary", values)

    @http.route(['/my/time_off'], type='http', auth="user", method='post', website=True)
    def portal_my_time_off(self, **post):
        values = self._prepare_portal_layout_values()
        user_id = request.env.user.id
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', user_id)])
        time_off = request.env['hr.leave'].sudo().search(
            [('employee_id', '=', employee.id)])
        types = request.env['hr.leave.type'].sudo().search(
            [('allocation_validation_type', 'in', ['officer', 'no', 'set'])])
        # types = request.env['hr.leave.type'].sudo().search(['&',('virtual_remaining_leaves','>',0),'|',('allocation_validation_type','in',['yes','no']),('max_leaves','>','0')])
        error = []
        if 'submit' in post:
            time_off_type_options = []
            for option in types:
                time_off_type_options.append(_(option.id))
            if post.get('time_off_type'):
                time_off_type = post['time_off_type'].strip()
                if time_off_type not in time_off_type_options:
                    raise UserError(_('Please choose a valid time off type.'))
                    # error["time_off_type"] = _('Please choose a valid time off type')
            if error:
                pass

            else:
                try :
                    date_to = datetime.strptime(post['date_to'], '%Y-%m-%d')
                    date_from = datetime.strptime(post['date_from'], '%Y-%m-%d')
                    m = date_to - date_from

                    time_off_id = request.env['hr.leave'].sudo().create({
                        'request_date_from': date_from.date(),
                        'request_date_to': date_to.date(),
                        'holiday_status_id': int(time_off_type),
                        'employee_id': employee.id,
                        'number_of_days': m.total_seconds() / (60 * 60 * 24),
                        'name': post['name'],
                    })
                except:
                    raise UserError(_('Set Correct  information'))
                return request.redirect('/my/time_off')

        values.update({
            'page_name': 'time_off',
            'error': error,
            'types': types,
            'time_off': time_off,
            'page_name': 'time off',
            'default_url': '/my/time_off',
        })
        return request.render("hr_self_service.portal_my_time_off", values)

    @http.route(['/my/leave_allocation'], type='http', auth="user", method='post', website=True)
    def portal_my_leave_allocation(self, **post):
        values = self._prepare_portal_layout_values()
        user_id = request.env.user.id
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', user_id)])
        leave_allocation = request.env['hr.leave.allocation'].sudo().search(
            [('employee_id', '=', employee.id)])
        types = request.env['hr.leave.type'].sudo().search(
            [('allocation_validation_type', '!=', 'no')])
        error = []
        if 'submit' in post:
            time_off_type_options = []
            for option in types:
                time_off_type_options.append(_(option.id))
            if post.get('time_off_type'):
                time_off_type = post['time_off_type'].strip()
                if time_off_type not in time_off_type_options:
                    raise UserError(_('Please choose a valid time off type.'))
                    # error["time_off_type"] = _('Please choose a valid time off type')
            if error:
                pass
            else:
                try:
                    leave_allocation_id = request.env['hr.leave.allocation'].sudo().create({
                        'name': post['name'],
                        'notes': post['reason'],
                        'holiday_status_id': int(time_off_type),
                        'employee_id': employee.id
                    })
                    print('\n\n\n\n\n\n\n\n', post['number_of_days_display'])
                    if leave_allocation_id.type_request_unit == 'hour':
                        leave_allocation_id.number_of_days = int(
                            post['number_of_days_display'])
                    if leave_allocation_id.type_request_unit == 'day':
                        leave_allocation_id.number_of_days = int(
                            post['number_of_days_display'])
                except:
                    raise UserError(_('Set Correct  information'))
                return request.redirect('/my/leave_allocation')

        values.update({
            'page_name': 'leave_allocation',
            'types': types,
            'leave_allocation': leave_allocation,
            'page_name': 'leave allocation',
            'default_url': '/my/leave_allocation',
        })
        return request.render("hr_self_service.portal_my_leave_allocation", values)

    @route(['/checkin/checkout'], type='http', auth="user", website=True)
    def checkin_checkout(self, **kw):
        user_id = request.env.user.id
        employee = request.env['hr.employee'].sudo().search([('user_id','=',user_id)])
        try:
            import geocoder
        except:
            UserError(_('You need to install python package: geocoder'))
        # location = geocoder.ip('me').latlng
        print("#################### kw ",kw)

        location = [kw['latitude'],kw['longitude']]
        employee.with_context(attendance_location=location)._attendance_action_change()
        return request.redirect('/hr/self/service')
