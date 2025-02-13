from odoo import api, models
import logging
_logger = logging.getLogger(__name__)

class AccountPaymentMethod(models.Model):
    _inherit = 'account.payment.method'

    @api.model
    def _get_payment_method_information(self):
        res = super()._get_payment_method_information()
        _logger.info("this is res %r",res)
        res['hyperpay'] = {'mode': 'unique', 'domain': [('type', '=', 'bank')]}
        return res
