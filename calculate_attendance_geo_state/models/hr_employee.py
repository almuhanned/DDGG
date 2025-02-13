# -*- encoding: utf-8 -*-
from odoo import fields, models,api,_
import math
from odoo.exceptions import UserError, ValidationError
import requests
import geocoder

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    def get_current_lat_lng(self):
        """Get current geolocationIP latitude and longitude.
           """
        ip = requests.get("https://ipecho.net/plain").text
        url = "http://api.ipstack.com/" + ip + "?access_key=" + "256f6e668afd710a5eb9a0137da5c248"
        response = requests.get(url).json()
        lat, lng = response['longitude'], response['latitude']
        return lat, lng
        # geolocation_req = requests.get('https://get.geojs.io/v1/ip/geo/' + current_ip + '.json')
        # geolocation_dict = geolocation_req.json()
        # return [geolocation_dict['latitude'],geolocation_dict['longitude']]

    def attendance_manual(self, next_action, entered_pin=False,
                          location=False):
        res = super(HrEmployee, self.with_context(
            attendance_location=location)).attendance_manual(
            next_action, entered_pin)
        return res

    def _attendance_action_change(self):
        res = super()._attendance_action_change()
        self.ensure_one()
        l = []
        dep_list = []
        attendance_geofence = self.env['hr.attendance.area'].search([('attendance_ok','=',True),('shape_paths','!=',{}),('employee_ids','=',self.id)])
        location = self.env.context.get('attendance_location', False)
        outgoing_server = self.env['ir.mail_server'].search([])
        emp_department = self.env['hr.department'].search([('member_ids','in',self.id)],limit=1)
        if location and attendance_geofence:
            if attendance_geofence.department_ids: 
                for department in attendance_geofence.department_ids:
                    dep_list.append(department.id)
            state = attendance_geofence._compute_geofence_state(float(location[0]),float(location[1]))
            if (self.attendance_state == 'checked_in' and attendance_geofence.department_ids and emp_department and emp_department.id in dep_list) or (self.attendance_state == 'checked_in' and not attendance_geofence.department_ids) or (self.attendance_state == 'checked_in' and not emp_department):
                res.write({
                    'check_in_lat': float(location[0]),
                    'check_in_lng': float(location[1]),
                    'geofence_id': attendance_geofence[0].id,
                    'check_in_geo_state': state
                })            
                if attendance_geofence[0].notify_user and attendance_geofence[0].type_notification == 'email':
                    if outgoing_server: 
                        for server in outgoing_server:
                            l.append(server.sequence)
                        seq = min(l)
                        outgoing_server_id = self.env['ir.mail_server'].search([('sequence','=',seq)])
                        if res['check_in_geo_state'] == 'in':
                            values = {
                                'email_to': self.user_id.login,
                                'email_from': self.company_id.email,
                                'subject': "Attendance Geofence State",
                                'body_html': ('%s checked-in at %s %s geofence area.') % (self.name,res['check_in'],res['check_in_geo_state']),
                                'mail_server_id': outgoing_server_id.id
                            }
                            mail_mail_obj = self.env['mail.mail'].create(values)
                            m = mail_mail_obj.send()
                        else:
                            raise ValidationError(_("You are out Geofence Area."))
                    else:
                        raise ValidationError(_("Please configure outgoing server."))
                            # else:
                #     sendsms
            elif (self.attendance_state == 'checked_out' and attendance_geofence.department_ids and emp_department and emp_department.id in dep_list) or (self.attendance_state == 'checked_in' and not attendance_geofence.department_ids) or (self.attendance_state == 'checked_in' and not emp_department):
                res.write({
                    'check_out_lat': float(location[0]),
                    'check_out_lng': float(location[1]),
                    'geofence_id': attendance_geofence[0].id,
                    'check_out_geo_state': state
                })
                if attendance_geofence[0].notify_user and attendance_geofence[0].type_notification == 'email':
                    if outgoing_server: 
                        for server in outgoing_server:
                            l.append(server.sequence)
                        seq = min(l)
                        outgoing_server_id = self.env['ir.mail_server'].search([('sequence','=',seq)])
                        if res['check_out_geo_state'] == 'in':
                            values = {
                                'email_to': self.user_id.login,
                                'email_from': self.company_id.email,
                                'subject': "Attendance Geofence State",
                                'body_html': ('%s checked-out at %s %s geofence area.') % (self.name,res['check_out'],res['check_out_geo_state']),
                                'mail_server_id': outgoing_server_id.id
                            }
                            mail_mail_obj = self.env['mail.mail'].create(values)
                            m = mail_mail_obj.send()
                        else:
                            raise ValidationError(_("You are out Geofence Area."))
                    else:
                        raise ValidationError(_("Please configure outgoing server."))
                # else:
                #     sendsms
            elif (attendance_geofence.department_ids and emp_department and emp_department.id not in dep_list) or (attendance_geofence.department_ids and not emp_department):
                raise ValidationError(_("You are not allowed to attendance, you are out of departments geofence."))
        elif location and not attendance_geofence:
            if self.attendance_state == 'checked_in':
                res.write({
                    'check_in_lat': float(location[0]),
                    'check_in_lng': float(location[1]),
                })
            else:
                res.write({
                    'check_out_lat': float(location[0]),
                    'check_out_lng': float(location[1]),
                })
        else:
            print("0000000///////")
        return res