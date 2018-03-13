# -*- coding: utf-8 -*- 
# Part of Odoo. See LICENSE file for full copyright and licensing details. 
from odoo import api, fields, models 
from datetime import datetime 

class scat_allergens(models.Model): 
    _name = 'ej.scat_allergens'
    _rec_name = 'allergens'

    allergens = fields.Char(string='allergens', required=True) 
 
    refinterna = fields.Char(string='refinterna', required=True) 
 
