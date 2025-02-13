# -*- coding: utf-8 -*-
#################################################################################
#
#    Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
#################################################################################
import re
import logging

import dateutil.parser
import pytz
from odoo import api, fields, models, _
from odoo.addons.payment.models.payment_acquirer import ValidationError
import pprint
from odoo.fields import Datetime

_logger = logging.getLogger(__name__)


class AcquirerHyperPay(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('hyperpay', 'HyperPay')], ondelete={'hyperpay': 'set default'})
    hyperpay_authorization = fields.Char('Authorization', required_if_provider='hyperpay', groups='base.group_user',
                                         help='Authorization header with Bearer authentication scheme')
    hyperpay_merchant_id = fields.Char(
        'Merchant Id', groups='base.group_user',
        help='The Merchant ID is required to authorize the request')

    #New method added to core
    def _get_default_payment_method_id(self):
        isd = self.env.ref('payment_hyperpay.payment_acquirer_hyperpay').id
        _logger.info("This is ids for data %r", isd)
        self.ensure_one()
        if self.provider != 'hyperpay':
            return super()._get_default_payment_method_id()
        return self.env.ref('payment_hyperpay.payment_method_hyperpay').id

    def hyperpay_form_generate_values(self, values):
        hyperpay_tx_values = dict(values)
        if values.get('reference', '/') != "/":
            tx = self.env['payment.transaction'].sudo().search([('reference', '=', values.get('reference'))])
            hyperpay_tx_values.update({
                "txId": tx.id
            })
        return hyperpay_tx_values


class HyperPayPaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    hyperpay_checkout_id = fields.Char('Checkout Id', groups='base.group_user',
                                       help='Unique checkout id for every hyper transasction')

    @api.model
    def _hyperpay_form_get_tx_from_data(self, data):
        reference = data.get('ndc')
        tx_id = data.get('tx_id')
        tx = tx_id and self.sudo().browse(int(tx_id))

        if not tx or len(tx) > 1:
            error_msg = _('received data for reference %s') % (pprint.pformat(reference))
            if not tx:
                error_msg += _('; no order found')
            else:
                error_msg += _('; multiple order found')
            _logger.info(error_msg)
            raise ValidationError(error_msg)

        return tx

    def _get_specific_rendering_values(self, processing_values):
        """ Override of payment to return Alipay-specific rendering values.
        Note: self.ensure_one() from `_get_processing_values`
        :param dict processing_values: The generic and specific processing values of the transaction
        :return: The dict of acquirer-specific processing values
        :rtype: dict
        """
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider != 'hyperpay':
            return res

        _logger.info('--specific------%r', (processing_values, self.reference))
        hyperpay_tx_values = {}
        tx = self.env['payment.transaction'].sudo().search([('reference', '=', self.reference)])
        _logger.info('--specific------%r', (processing_values, self.reference, tx.id))
        hyperpay_tx_values.update({
            "txId": tx.id,
            'reference': self.reference
        })
        return hyperpay_tx_values

    # def _process_feedback_data(self, data):
    #
    #     super()._process_feedback_data(data)
    #     if self.provider != 'hyperpay':
    #         return
    #
    #     _logger.info('Validated transfer payment for tx %s: set as pending' % (self.reference))
    #     result = data.get('result')
    #     result_code = result.get('code')
    #     res = {}
    #     success_pattern = [
    #         '^(000\.000\.|000\.100\.1|000\.[36])',
    #         '^(000\.400\.0[^3]|000\.400\.100)'
    #     ]
    #     pending_pattern = [
    #         '^(000\.200)',
    #         '^(800\.400\.5|100\.400\.500)'
    #     ]
    #     _logger.info('------feedback-%r', result)
    #     if re.match(success_pattern[0], result_code) or re.match(success_pattern[1], result_code):
    #         date_validate = dateutil.parser.parse(data.get('timestamp')).astimezone(pytz.utc).replace(tzinfo=None)
    #         res.update(acquirer_reference=data.get('id'), last_state_change=date_validate,
    #                    state_message=result.get('description', ''))
    #         self._set_done()
    #     elif re.match(pending_pattern[0], result_code) or re.match(pending_pattern[1], result_code):
    #         res.update(state_message=result.get('description', ''))
    #         self._set_pending()
    #     elif re.match('/^(000\.100\.2)/', result_code):
    #         res.update(state_message=result.get('description', ''))
    #         self._set_error(result.get('description', ''))
    #     else:
    #         res.update(state_message=result.get('description', ''))
    #         self._set_canceled()
    #     _logger.info('------feedback-%r', (res, self.write(res), self))
    #     return self.write(res)
