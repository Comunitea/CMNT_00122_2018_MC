# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import UserError


class scat_expediente(models.Model):

    _name = "scat.expediente"

    n_expediente = fields.Integer(string="Nº de expediente", required= True, readonly=True, states={'borrador': [('readonly', False)]})
    partner_id= fields.Many2one('res.partner', 'Cliente', required=True, readonly=True, states={'borrador': [('readonly', False)]})
    start_date = fields.Date(string="Fecha inicio", required=True, readonly=True, states={'borrador': [('readonly', False)]})
    end_date = fields.Date("Fecha de fin", readonly=True, states={'borrador': [('readonly', False)]})
    school_ids = fields.Many2many('scat.school', relation='scat_expediente_scat_school_rel',
        column2='scat_school_id', column1='scat_expediente_id', string="Colegio/s", readonly=True, states={'borrador': [('readonly', False)]})
    state= fields.Selection([ ("borrador", "Borrador"),("open","Abierto"),("close", "Cerrado")], "Estado", default="borrador", readonly=True)

    company_id = fields.Many2one('res.company', 'Company', required=True,
                                 default=lambda s: s.env.user.company_id.id, readonly=True, states={'borrador': [('readonly', False)]})

    journal_kids_id = fields.Many2one("account.journal", "Diario Niños", domain=[("type","=", "sale")])
    journal_ise_id = fields.Many2one("account.journal", "Diario Ise", domain=[("type","=", "sale")])

    product_ids = fields.One2many('scat.expediente.product', 'expediente_id', string ="Productos")


    @api.multi
    def get_invoice_lines(self):
        self.ensure_one()
        res = []
        for line in self.product_ids:
            product = self.env['product.product'].with_context(force_company = self.company_id.id).browse(line.product_id.id)
            if product.property_account_income_id:
                account = product.property_account_income_id.id
            elif product.categ_id.property_account_income_categ_id:
                account = product.categ_id.property_account_income_categ_id.id
            else:
                raise UserError("No se ha encontrado una cuenta de ingreso para el producto %s" % product.name)
            res.append({'product_id': product.id,
                        'price_unit': line.price_u,
                        'name': product.name,
                        'invoice_line_tax_ids': [(6,0,line.impuestos_ids.ids)],
                        'account_id': account,
                        'uom_id': product.uom_id.id})
        return res


    @api.multi
    def abrir_expediente(self):

        for exp in self:

            new_state = "open"
            exp.state = new_state
            for school in exp.school_ids:

                expedientes= self.search([('id', '!=', exp.id),('school_ids', 'in', [school.id]), ('state', '=', 'open')])
                if expedientes:
                    raise UserError("No se ha podido abrir el expediente porque el colegio %s se escuentra en otro expediente abierto %s" %(school.name, expedientes[0].n_expediente) )
