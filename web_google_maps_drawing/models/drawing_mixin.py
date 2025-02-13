# -*- encoding: utf-8 -*-
from odoo import api, fields, models
from odoo.tools import safe_eval

class GoogleMapsDrawingShapeMixin(models.Model):
    _name = 'google_maps.drawing.shape.mixin'
    _description = 'Google Maps Shape Mixin'
    _rec_name = 'shape_name'

    shape_name = fields.Char(string='Name' ,required=True)
    shape_area = fields.Float(string='Area')
    poly_lat = fields.Char(string='Polygon Latitude')
    poly_lng = fields.Char(string='Polygon Longitude')
    shape_radius = fields.Float(string='Radius',digits=(16, 5))
    shape_description = fields.Text(string='Description')
    shape_type = fields.Selection([
        ('circle', 'Circle'), ('polygon', 'Polygon'),
        ('rectangle', 'Rectangle')], string='Type', default='polygon', 
        required=True)
    center_latitude = fields.Float(string='Center Latitude',digits=(16, 5))
    center_longitude = fields.Float(string='Center Longitude',digits=(16, 5))
    NE_latitude = fields.Float(string='NorthEast Latitude',digits=(16, 5))
    NE_longitude = fields.Float(string='NorthEast Longitude',digits=(16, 5))
    SW_latitude = fields.Float(string='SouthWest Latitude',digits=(16, 5))
    SW_longitude = fields.Float(string='SouthWest Longitude',digits=(16, 5))
    shape_paths = fields.Text(string='Paths')

    def decode_shape_paths(self):
        self.ensure_one()
        return safe_eval(self.shape_paths)