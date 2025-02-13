from odoo import models, api, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    eos_id = fields.Many2one('end.of.service.award', compute='get_eos', store=True)

    @api.depends('name')
    def get_eos(self):
        for rec in self:
            rec.eos_id = self.env['end.of.service.award'].search([('account_move_id', '=', rec.id)])

    def open_eos(self):
        return {
            'name': 'EOS',
            'type': 'ir.actions.act_window',
            'res_model': 'end.of.service.award',
            'view_mode': 'form',
            'res_id': self.eos_id.id,
            'context': {'create': False},
        }