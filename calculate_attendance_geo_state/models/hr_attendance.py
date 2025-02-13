# -*- encoding: utf-8 -*-
from odoo import fields, models,api,_
import math
from odoo.exceptions import UserError, ValidationError
from shapely.geometry import Point, Polygon
import requests

class HrAttendance(models.Model):
	_inherit = 'hr.attendance'

	check_in_lat = fields.Float(string='Check-in Latitude', digits=(16, 5))
	check_in_lng = fields.Float(string='Check-in Longitude', digits=(16, 5))
	check_out_lat = fields.Float(string='Check-out Latitude', digits=(16, 5))
	check_out_lng = fields.Float(string='Check-out Longitude', digits=(16, 5))
	check_in_geo_state = fields.Selection([
		('in', 'In'), ('out', 'Out')], string='Check-in State')
	check_out_geo_state = fields.Selection([
		('in', 'In'), ('out', 'Out')], string='Check-out State')
	geofence_id = fields.Many2one('hr.attendance.area', string='Geofence Area')
	# id = fields.Char(string='ID', related='employee_id.id')
	emp_id = fields.Integer(string='ID', related='employee_id.id')
	email = fields.Char(string='Email', related='employee_id.work_email')
	company = fields.Many2one('res.company', srting='Company', related='employee_id.company_id')
	active = fields.Boolean(string='Active', related='employee_id.active')

class HrAttendanceArea(models.Model):
	""" Inherit Drawing mixins model 'google_maps.drawing.shape.mixin' """
	_name = 'hr.attendance.area'
	_inherit = ['mail.thread', 'google_maps.drawing.shape.mixin']
	_description = 'Attendance Area'

	notify_user = fields.Boolean("Send Notification") 
	type_notification = fields.Selection([
		('email', 'Email'), ('sms', 'SMS')], default='email', string='Type of Notification')
	current_user = fields.Many2one('res.users','Current User', default=lambda self: self.env.user)
	company_id = fields.Many2one('res.company','Company', default=lambda self: self.env.user.company_id.id)
	attendance_ok = fields.Boolean('Selected on Attendance')
	department_ids = fields.Many2many('hr.department', string='Departments')
	employee_ids = fields.Many2many('hr.employee',string='Employees')
	state = fields.Selection([
		('in', 'In'), ('out', 'Out')], string='State')

	@api.constrains('employee_ids')
	def check_geo_attendance(self):
		for rec in self.employee_ids:
			attendance_geo_id = self.env['hr.attendance.area'].search([('attendance_ok','=',True),('employee_ids','=',rec.id)])
			if len(attendance_geo_id) > 1:
				raise ValidationError(_("Attendance Geofence must be Only One"))

	def _compute_geofence_state(self, latitude, longitude):
		state = ''
		for rec in self:
			rec.state='in'
			#Compute geofence state of drawing circle shape type which depends on current location
			if rec.shape_type == 'circle':
				R = 6372800  # Earth radius in meters
				phi1, phi2 = math.radians(latitude), math.radians(rec.center_latitude) 
				dphi = math.radians(rec.center_latitude - latitude)
				dlambda = math.radians(rec.center_longitude - longitude)
				a = (math.sin(dphi/2)**2) + (math.cos(phi1)*math.cos(phi2)*(math.sin(dlambda/2)**2))
				distance = 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a))
				if distance <= rec.shape_radius:
					state = rec.state = 'in'
				else: 
					state = rec.state = 'out'
			#Compute geofence state of drawing rectangle shape type which depends on current location
			elif rec.shape_type == 'rectangle':
				if latitude >= rec.SW_latitude and latitude <= rec.NE_latitude and longitude >= rec.SW_longitude and longitude <= rec.NE_longitude:
					state = rec.state = 'in'
				else:
					state = rec.state = 'out'
			#Compute geofence state of drawing polygon shape type which depends on current location
			elif rec.shape_type == 'polygon':
				pt = Point(latitude, longitude)
				vertices_y = []
				vertices_x = []
				poly_lat = str(rec.poly_lat)
				poly_lat_1 = poly_lat.split(',')
				poly_lng = str(rec.poly_lng)
				poly_lng_1 = poly_lng.split(',')
				tuple_lat_lng = []
				k = 0
				if rec.poly_lat:
					for m in poly_lat_1:
						if m:
							vertices_y.append(float(m))
					for n in poly_lng_1:
						if n:
							vertices_x.append(float(n))
					for i in range(len(vertices_y)):
						m = vertices_y[k]
						tuple_lat_lng.append(tuple([vertices_y[k],vertices_x[k]]))
						k+=1
					poly = Polygon(tuple_lat_lng)
					k = poly.contains(pt)
					if k:
						state = rec.state='in'
					else:
						state = rec.state='out'
		if rec.state =='out':
			raise ValidationError(_('You are out of allowed attendance area'))
		else:

			return state