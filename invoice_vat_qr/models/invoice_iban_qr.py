# -*- coding: utf-8 -*-
import qrcode
import base64
from io import BytesIO
from odoo import models, api, fields, _
import binascii


class AccountMoveLineInherit(models.Model):
    _inherit = 'account.move.line'
    _order = 'account_id ASC'
    tax_amount = fields.Float(string="Tax Amount", compute="_compute_tax_amount")

    @api.depends('tax_ids', 'price_unit', 'quantity')
    def _compute_tax_amount(self):
        for line in self:
            if line.tax_ids:
                line.tax_amount = line.price_total - line.price_subtotal
            else:
                line.tax_amount = 0.0


class AccountMoveInherit(models.Model):
    _inherit = "account.move"

    def action_send_invoice_directly(self):
        invoice_object = self
        template = self.env.ref('account.email_template_edi_invoice', raise_if_not_found=False)
        lang = False
        if template:
            lang = template._render_lang(invoice_object.ids)[invoice_object.id]

        ctx = dict(
            mark_invoice_as_sent=True,
            active_ids=invoice_object.ids,
            custom_layout="mail.mail_notification_paynow",
            model_description=invoice_object.with_context(lang=invoice_object.partner_id.lang).type_name,
            force_email=True,
            default_res_model='account.move',
            default_use_template=bool(template),
        )
        values = {
            'model': 'account.move',
            'res_id': invoice_object.id,
            'template_id': template and template.id or False,
            'composition_mode': 'comment',
        }

        wizard = self.env['account.invoice.send'].with_context(ctx).create(values)
        wizard._compute_composition_mode()
        wizard.onchange_template_id()
        wizard.onchange_is_email()
        wizard._send_email()

    def send_online_invoice(self):
        for rec in self:
            rec.action_send_invoice_directly()

    def action_post(self):
        try:
            self.send_online_invoice()
        except:
            pass

        return super(AccountMoveInherit, self).action_post()

    @api.onchange('partner_id')
    def _onchange_partner_warning_vat(self):
        if not self.partner_id:
            return
        partner = self.partner_id
        warning = {}
        if partner.company_type == 'company' and not partner.vat:
            title = ("Warning for %s") % partner.name
            message = _("Please add VAT ID for This Partner '%s' !") % (partner.name)
            warning = {
                'title': title,
                'message': message,
            }
        if warning:
            res = {'warning': warning}
            return res

    def _string_to_hex(self, value):
        if value:
            string = str(value)
            string_bytes = string.encode("UTF-8")
            encoded_hex_value = binascii.hexlify(string_bytes)
            hex_value = encoded_hex_value.decode("UTF-8")
            # print("This : "+value +"is Hex: "+ hex_value)
            return hex_value

    def _get_hex(self, tag, length, value):
        if tag and length and value:
            # str(hex(length))
            hex_string = self._string_to_hex(value)
            length = int(len(hex_string) / 2)
            # print("LEN", length, " ", "LEN Hex", hex(length))
            conversion_table = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
            hexadecimal = ''
            while (length > 0):
                remainder = length % 16
                hexadecimal = conversion_table[remainder] + hexadecimal
                length = length // 16
            # print(hexadecimal)
            if len(hexadecimal) == 1:
                hexadecimal = "0" + hexadecimal
            return tag + hexadecimal + hex_string

    def get_qr_code_data(self):
        if self.move_type in ('out_invoice', 'out_refund'):
            sellername = str(self.company_id.name)
            seller_vat_no = self.company_id.vat or ''
            if self.partner_id.company_type == 'company':
                customer_name = self.partner_id.name
                customer_vat = self.partner_id.vat
        else:
            sellername = str(self.partner_id.name)
            seller_vat_no = self.partner_id.vat
        seller_hex = self._get_hex("01", "0c", sellername)
        vat_hex = self._get_hex("02", "0f", seller_vat_no) or ""
        time_stamp = str(self.create_date)
        date_hex = self._get_hex("03", "14", time_stamp)
        total_with_vat_hex = self._get_hex("04", "0a", str(round(self.amount_total, 2))) or 0
        total_vat_hex = self._get_hex("05", "09", str(round(self.amount_tax, 2))) or 0
        print(vat_hex)
        qr_hex = seller_hex + vat_hex + date_hex + total_with_vat_hex + total_vat_hex
        encoded_base64_bytes = base64.b64encode(bytes.fromhex(qr_hex)).decode()
        return encoded_base64_bytes

    qr_code = fields.Binary(string="QR Code", attachment=True, compute="generate_qr_code")

    @api.onchange('invoice_line_ids.product_id')
    def generate_qr_code(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.get_qr_code_data())
        qr.make(fit=True)
        img = qr.make_image()
        temp = BytesIO()
        img.save(temp, format="PNG")
        qr_image = base64.b64encode(temp.getvalue())
        self.qr_code = qr_image


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    @api.onchange('partner_id')
    def _onchange_partner_warning_vat(self):
        if not self.partner_id:
            return
        partner = self.partner_id
        warning = {}
        if partner.company_type == 'company' and not partner.vat:
            title = ("Warning for %s") % partner.name
            message = _("Please add VAT ID for This Partner '%s' !") % (partner.name)
            warning = {
                'title': title,
                'message': message,
            }
        if warning:
            res = {'warning': warning}
            return res
#
#
# class PurchaseOrderInherit(models.Model):
#     _inherit = 'purchase.order'
#
#     @api.onchange('partner_id')
#     def _onchange_partner_warning_vat(self):
#         if not self.partner_id:
#             return
#         partner = self.partner_id
#         warning = {}
#         if partner.company_type == 'company' and not partner.vat:
#             title = ("Warning for %s") % partner.name
#             message = _("Please add VAT ID for This Partner '%s' !") % (partner.name)
#             warning = {
#                 'title': title,
#                 'message': message,
#             }
#         if warning:
#             res = {'warning': warning}
#             return res
