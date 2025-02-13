from odoo import models, fields

class Employee(models.Model):
    _inherit = 'hr.employee'

    discount_limit = fields.Float(string="Employee Discount", help="Maximum discount an employee can apply without approval.")
    approval_manager_id = fields.Many2one('hr.employee', string="Approval Manager", help="Manager responsible for approving discounts beyond the employee's limit.")
