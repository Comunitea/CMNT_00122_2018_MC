# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools
from zeep import Client
from lxml import objectify
from datetime import datetime


class ResCompany(models.Model):

    _inherit = "res.company"

    ise_login = fields.Char("Usuario ISE")
    ise_password = fields.Char(u"Contraseña ISE")


class ScatSchoolIseIntegration(models.Model):

    _name = "scat.school.ise.integration"
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _rec_name = "call_date"
    _order = "call_date desc"

    call_date = fields.Datetime(u"Fecha de conexión", required=True,
                                default=fields.Datetime.now)
    fail = fields.Boolean("Error")
    token = fields.Char("Token", readonly=True)
    operation = fields.Char(u"Operación", required=True)
    company_id = fields.Many2one("res.company", u"Compañía", readonly=True,
                                 default=lambda s: s.env.user.company_id.id)

    @api.multi
    def _get_pricelist_item(self, child):
        pricelist_item = self.env['product.pricelist.item'].\
            search([('percent_price', '=', child.BONIFICACIONISE)])
        if not pricelist_item:
            self.message_post(body=u"Cree una tarifa de venta con una "
                              u"bonificación de %s." %
                              str(child.BONIFICACIONISE),
                              message_type='comment')
        return pricelist_item

    @api.multi
    def _get_parent_vals(self, child):
        return {'x_ise_estado': 'titular',
                'is_company': True,
                'company_id': False,
                'customer': True,
                'street': child.DIRECCION,
                'zip': child.CP,
                'city': child.MUNICIPIO,
                'state_id':
                (child.CP and self.env['res.better.zip'].
                 search([('name', '=', child.CP)])) and
                self.env['res.better.zip'].
                search([('name', '=', child.CP)])[0].state_id.id or False,
                'x_ise_nie': child.NIFTITULAR,
                'phone': child.TELEFONO,
                'email': child.EMAIL,
                'name': child.NOMBRETITULAR + u" " + child.APELLIDOSTITULAR}

    @api.multi
    def _set_acc_number(self, parent, child_data, country, exp,
                        cancel_on_change=False):
        acc_number = str(child_data.CUENTABANCARIA).replace("-", "")
        bank = self.env['res.partner.bank'].\
            search([('acc_number', '=', acc_number),
                    ('partner_id', '=', parent.id)])
        if not bank:
            if cancel_on_change:
                mandates = self.env['account.banking.mandate'].\
                    search([('partner_id', '=', parent.id)])
                if mandates:
                    mandates.cancel()
                    self.message_post(body=u"Se ha cancelado un mandato para "
                                      u"empresa %s por cambio de cuenta. "
                                      u"Revisad los efectos pendientes de "
                                      u"remesar." % parent.name,
                                      message_type='comment')
            bank_vals = {'acc_number': acc_number,
                         'partner_id': parent.id,
                         'company_id': False,
                         'acc_country_id': country.id}
            bank = self.env['res.partner.bank'].create(bank_vals)
            bank._onchange_acc_number_l10n_es_partner()
            mandate = self.env['account.banking.mandate'].\
                create({'company_id': exp.company_id.id,
                        'format': 'sepa',
                        'partner_bank_id': bank.id,
                        'scheme': 'CORE',
                        'recurrent_sequence_type': 'recurring',
                        'type': 'recurrent',
                        'signature_date':
                        datetime.strptime(str(child_data.FECHADESDESERVICIO),
                                          '%d/%m/%Y').strftime('%Y-%m-%d')})
            mandate.validate()

    @api.multi
    def _try_write_vat(self, parent, country, child):
        if child.NIFTITULAR:
            try:
                parent.write({'vat': (country and country.code or u"ES") +
                              str(child.NIFTITULAR).replace("-", "")})
            except Exception:
                self.message_post(body=u"NIF %s no válido para el titular %s" %
                                  ((country and country.code or u"ES") +
                                   str(child.NIFTITULAR).replace("-", ""),
                                   parent.name), message_type='notification')
        else:
            self.message_post(body=u"En el ISE no figura el nif para el "
                                   u"titular %s" % parent.name,
                              message_type='notification')

    @api.multi
    def _update_parent_data(self, parent, child_data):
        update_vals = {}
        if parent.street != child_data.DIRECCION:
            update_vals['street'] = child_data.DIRECCION
        if parent.zip != child_data.CP:
            update_vals['zip'] = child_data.CP
            update_vals['state_id'] = \
                (child_data.CP and self.env['res.better.zip'].
                 search([('name', '=', child_data.CP)])) and \
                self.env['res.better.zip'].\
                search([('name', '=', child_data.CP)])[0].state_id.id or False
        if parent.city != child_data.MUNICIPIO:
            update_vals['city'] = child_data.MUNICIPIO
        if parent.phone != child_data.TELEFONO:
            update_vals['phone'] = child_data.TELEFONO
        if parent.email != child_data.EMAIL:
            update_vals['email'] = child_data.EMAIL
        if parent.name != child_data.NOMBRETITULAR + u" " + \
                child_data.APELLIDOSTITULAR:
            update_vals['name'] = child_data.NOMBRETITULAR + u" " + \
                child_data.APELLIDOSTITULAR
        if update_vals:
            parent.write(update_vals)

    @api.multi
    def _create_student_school(self, child, child_data, school, exp):
        school_vals = {'start_date':
                       datetime.strptime(str(child_data.FECHADESDESERVICIO),
                                         '%d/%m/%Y').strftime('%Y-%m-%d'),
                       'school_id': school.id,
                       'company_name': exp.company_id.name,
                       'student_id': child.id}
        self.env['scat.school.student'].create(school_vals)

    @api.multi
    def _update_child_data(self, child, child_data):
        update_vals = {}
        if child.name != child_data.NOMBRE + u" " + child_data.APELLIDOS:
            update_vals['name'] = child_data.NOMBRE + u" " + \
                child_data.APELLIDOS
        if child_data.NIVELEDUCATIVO and self.env['scat.course'].\
                search([('name', 'ilike',
                         tools.ustr(child_data.NIVELEDUCATIVO))]):
            course = self.env['scat.course'].\
                search([('name', 'ilike',
                         tools.ustr(child_data.NIVELEDUCATIVO))])[0]
            if child.course_id.id != course.id:
                update_vals['course_id'] = course.id
        if update_vals:
            child.write(update_vals)

    @api.multi
    def check_child_data(self, child_data, child, school, exp):
        open_schools = child.school_ids.filtered(lambda x: not x.end_date)
        if school.id != child.active_school_id.id:
            if open_schools:
                open_schools.\
                    write({'end_date':
                           datetime.
                           strptime(str(child_data.FECHADESDESERVICIO),
                                    '%d/%m/%Y').strftime('%Y-%m-%d')})
                self.message_post(body=u"Se ha finalizado un colegio para el "
                                       u"niño %s por cambio de colegio. "
                                       u"Revisad el control de presencia "
                                       u"actual y crear el nuevo."
                                       % child.name, message_type='comment')
            self._create_student_school(child, child_data, school, exp)
        elif child_data.FECHAHASTASERVICIO and open_schools:
            open_schools.write({'end_date':
                                datetime.
                                strptime(str(child_data.FECHAHASTASERVICIO),
                                         '%d/%m/%Y').
                                strftime('%Y-%m-%d')})

        pricelist_item = self._get_pricelist_item(child_data)
        if not pricelist_item:
            self.fail = True
            return
        if child_data.CUENTABANCARIA:
            country = self.env['res.country'].\
                search([('code', '=', str(child_data.CUENTABANCARIA)[:2])],
                       limit=1)[0]
        else:
            country = False
            self.message_post(body=u"La actualización del niño %s desde el ISE"
                                   u" viene sin cuenta bancaria."
                                   % child.name, message_type='comment')

        parent = self.env['res.partner'].search([('x_ise_nie', '=',
                                                  child_data.NIFTITULAR)])
        if parent:
            if parent[0].id != child.parent_id.id:
                child.parent_id = parent[0].id
            parent = parent[0]
            self._update_parent_data(parent, child_data)
            if country and parent.country_id.id != country.id:
                parent.country_id = country.id
        else:
            parent_vals = self._get_parent_vals(child_data)
            parent_vals['property_product_pricelist'] = \
                pricelist_item.pricelist_id.id
            parent_vals['country_id'] = country and country.id or False
            parent = self.env['res.partner'].create(parent_vals)
            child.parent_id = parent.id
            self._try_write_vat(parent, country, child_data)

        if pricelist_item.pricelist_id.id != \
                child.parent_id.property_product_pricelist.id:
            child.parent_id.property_product_pricelist = \
                pricelist_item.pricelist_id.id

        if child_data.CUENTABANCARIA:
            self._set_acc_number(parent, child_data, country, exp)
        self._update_child_data(child, child_data)

    @api.multi
    def create_new_child(self, child, school, exp):
        pricelist_item = self._get_pricelist_item(child)
        if not pricelist_item:
            self.fail = True
            return
        if child.CUENTABANCARIA:
            country = self.env['res.country'].\
                search([('code', '=', str(child.CUENTABANCARIA)[:2])],
                       limit=1)[0]
        else:
            country = False
            self.message_post(body=u"La creación del niño con NIE %s "
                                   u"se está hacienod sin cuenta bancaria."
                                   % child.NIE, message_type='comment')
        parent = self.env['res.partner'].search([('x_ise_nie', '=',
                                                  child.NIFTITULAR)])

        if parent:
            parent = parent[0]
        else:
            parent_vals = self._get_parent_vals(child)
            parent_vals['property_product_pricelist'] = \
                pricelist_item.pricelist_id.id
            parent_vals['country_id'] = country and country.id or False
            parent = self.env['res.partner'].create(parent_vals)
            self._try_write_vat(parent, country, child)

        if child.CUENTABANCARIA:
            self._set_acc_number(parent, child, country, exp)

        child_vals = {'x_ise_nie': child.NIE,
                      'x_ise_estado': 'usuario',
                      'parent_id': parent.id,
                      'company_id': False,
                      'name': child.NOMBRE + u" " + child.APELLIDOS,
                      'course_id': (child.NIVELEDUCATIVO and
                                    self.env['scat.course'].
                                    search([('name', 'ilike',
                                             tools.
                                             ustr(child.NIVELEDUCATIVO))])) and
                      self.env['scat.course'].
                      search([('name', 'ilike',
                               tools.ustr(child.NIVELEDUCATIVO))])[0].id
                      or False}
        child_partner = self.env['res.partner'].create(child_vals)

        self._create_student_school(child_partner, child, school, exp)

    @api.multi
    def action_ise_load_childs(self):
        self.ensure_one()
        ise_url = self.env['ir.config_parameter'].\
            get_param('ise.webservice.url')
        client = Client(ise_url)
        token = client.service.loginISE(self.company_id.ise_login,
                                        self.company_id.ise_password,
                                        self.company_id.vat.replace("ES", ""))
        if not token:
            self.respose = u"Error de conexión"
            return
        self.token = token
        expedients = self.env["scat.expediente"].search([('company_id', '=',
                                                          self.company_id.id),
                                                         ('state', '=',
                                                          'open')])
        for exp in expedients:
            for school in exp.school_ids:
                child_data = client.service.infoAlumnos(exp.n_expediente,
                                                        exp.n_lote,
                                                        school.code,
                                                        token)
                xml = objectify.fromstring(child_data.encode('utf-8'))
                if xml.ERROR:
                    self.fail = True
                    self.message_post(body=u"Error %s: procesando el colegio "
                                      u"%s para el expediente %s." %
                                      (xml.ERROR, school.name,
                                       exp.display_name),
                                      message_type='comment')
                for child in xml.ALUMNOS.ALUMNODTO[0]:
                    if child.ESTADO == 'USUARIO':
                        exists = self.env["res.partner"].\
                            search([('x_ise_nie', '=', child.NIE)])
                        if not exists:
                            self.create_new_child(child, school, exp)
                        else:
                            self.check_child_data(child, exists[0], school,
                                                  exp)

    @api.model
    def action_sync_children(self):
        companies = self.env["res.company"].\
            search([('ise_login', '!=', False)])
        for company in companies:
            rec = self.create({'company_id': company.id,
                               'operation': "infoAlumnos"})
            rec.action_ise_load_childs()
