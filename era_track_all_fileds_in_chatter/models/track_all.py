from odoo import fields, models, tools
import logging
_logger = logging.getLogger(__name__)

class ir_model(models.Model):
    _inherit = "ir.model"

    track = fields.Boolean('Track Any Fields', help='Track any update on the chatter')

class mail_thread(models.AbstractModel):
    _inherit = 'mail.thread'

    @tools.ormcache('self.env.uid', 'self.env.su')
    def _get_tracked_fields(self):
        if self.env['ir.model']._get(self._name).track:
            fields = {name for name, field in self._fields.items()}
            return fields and set(self.fields_get(fields))
        else:
            return super(mail_thread, self)._get_tracked_fields()



