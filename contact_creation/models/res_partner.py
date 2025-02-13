from odoo import api, fields, models, tools, http, release, registry, _
from odoo.exceptions import ValidationError, Warning
from odoo.osv import expression
from lxml import etree
import json


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def unlink(self):
        """
            Override unlink method
        :return: Super Method
        """

        if not self.env.user.has_group("contact_creation.group_contact_creation"):
            raise ValidationError(_("You do not have the authority to delete a partner \nPlease contact system administrator"))
        return super(ResPartner, self).unlink()

    # @api.model_create_multi
    # def create(self, values):
    #     """
    #         Override create method
    #     :param values:
    #     :return: record ID
    #     """
    #
    #     if not self.env.user.has_group("contacts_partner_code.group_create_partner"):
    #         raise ValidationError(_("You do not have the authority to create a partner \nPlease contact system administrator"))
    #     return super(ResPartner, self).create(values)

    # def write(self, values):
    #     """
    #         Override write method
    #     :param values:
    #     :return: record ID
    #     """
    #
    #     if not self.env.user.has_group("contacts_partner_code.group_create_partner"):
    #         raise ValidationError(_("You do not have the authority to update a partner \nPlease contact system administrator"))
    #     return super(ResPartner, self).write(values)

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        result = super(ResPartner, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        access_group = self.env.user.has_group('contact_creation.group_contact_creation')
        arch = etree.XML(result['arch'])
        if view_type == 'tree':
            for node in arch.xpath("//tree"):
                node.set('create', '0')
                if access_group:
                    node.set('create', '1')
        if view_type == 'form':
            for node in arch.xpath("//form"):
                node.set('create', '0')
                if access_group:
                    node.set('create', '1')

        if view_type == 'kanban':
            for node in arch.xpath("//kanban"):
                node.set('create', '0')
                if access_group:
                    node.set('create', '1')
        result['arch'] = etree.tostring(arch, encoding='unicode')
        return result
