# -*- coding: utf-8 -*-
from odoo import fields, models, api


class AccountInvoiceLine(models.Model):

    _inherit='account.invoice.line'

    scat_student_id=fields.Many2one('scat.student', string = "scat_student")
    discount_line= fields.Boolean('Discount line', default = False)

class AccountInvoice(models.Model):

    _inherit='account.invoice'

    ise=fields.Boolean('ise')
