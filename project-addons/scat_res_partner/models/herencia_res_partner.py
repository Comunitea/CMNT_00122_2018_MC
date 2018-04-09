# -*- coding: utf-8 -*- 
# Part of Odoo. See LICENSE file for full copyright and licensing details. 
from odoo import api, fields, models 
from datetime import datetime 

class herencia_res_partner(models.Model): 
    _inherit = "res.partner" 
    x_ise_nie = fields.Char(string='x_ise_nie', required=False)  
    x_ise_estado = fields.Char(string='x_ise_estado', required=False)  
    x_ise_centro = fields.Char(string='x_ise_centro', required=False) 
 
    y_ise_factura_aut = fields.Boolean(string='y_ise_factura_aut', required=False) 
 
    y_ise_l = fields.Boolean(string='y_ise_l', required=False)  
    y_ise_m = fields.Boolean(string='y_ise_m', required=False)  
    y_ise_x = fields.Boolean(string='y_ise_x', required=False)  
    y_ise_j = fields.Boolean(string='y_ise_j', required=False)  
    y_ise_v = fields.Boolean(string='y_ise_v', required=False)  
    y_ise_s = fields.Boolean(string='y_ise_s', required=False) 
 
