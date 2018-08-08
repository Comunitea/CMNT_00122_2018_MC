# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from dateutil.relativedelta import relativedelta
from datetime import datetime


class ScatMenuType(models.Model):

    _name = "scat.menu.type"

    name = fields.Char("Nombre", size=80, required=True)
    conflict_allergens_ids = fields.Many2many('scat.allergens',
                                              string=u"Alérgenos conflictivos")


class ScatMenuConfig(models.Model):

    _name = "scat.menu.config"

    name = fields.Char("Nombre", size=140, required=True,
                       states={'done': [('readonly', False)]})
    menu_line_ids = fields.One2many('scat.menu.config.line', "menu_config_id",
                                    "Lineas",
                                    states={'done': [('readonly', False)]})
    state = fields.Selection([('draft', 'Borrador'), ('open', 'En progreso'),
                              ('done', 'Terminado')], "Estado", required=True,
                             default="draft", readonly=True)

    @api.multi
    def action_open(self):
        self.state = 'open'

    @api.multi
    def action_done(self):
        self.state = 'done'


class ScatMenuConfigLine(models.Model):

    _name = "scat.menu.config.line"

    product_id = fields.Many2one('product.product', 'Plato',
                                 domain=[('type', '!=', 'service')])
    name = fields.Char("Nombre", size=140, required=True)
    mtype_ids = fields.Many2many('scat.menu.type', string="Tipos",
                                 required=True)
    mode = fields.Selection([('fst_course', 'Primer plato'),
                             ('scnd_course', 'Segundo plato'),
                             ('garniture', u'Guarnición'),
                             ('bread', 'Pan'), ('dessert', 'Postre'),
                             ('drink', 'Bebida')],
                            'Momento', required=True)
    product_qty = fields.Float("Cant.", required=True, default=1.0)
    menu_config_id = fields.Many2one('scat.menu.config', u"Menú")

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.name = self.product_id.name

    @api.constrains('product_id', 'mtype_ids')
    def _check_allergens(self):
        for line in self:
            if line.product_id and line.product_id.allergens_ids:
                for typ in line.mtype_ids.filtered('conflict_allergens_ids'):
                    res = set(typ.conflict_allergens_ids.ids).\
                        intersection(line.product_id.allergens_ids.ids)
                    if res:
                        raise exceptions.\
                            ValidationError(u"Este plato %s es incompatible "
                                            u"con el tipo de menú, revise "
                                            u"los alérgenos." %
                                            line.product_id.name)

    @api.constrains('mode', 'mtype_ids')
    def _check_mode_mtype_config(self):
        for line in self:
            if line.menu_config_id:
                for mtype in line.mtype_ids:
                    res = self.search([('menu_config_id', '=',
                                        line.menu_config_id.id),
                                       ('id', '!=', line.id),
                                       ('mode', '=', line.mode),
                                       ('mtype_ids', 'in', [mtype.id])])
                    if res:
                        raise exceptions.\
                            ValidationError(u"No se puede repetir el tipo de "
                                            u"menú para el mismo momento")


class ScatMenuRotative(models.Model):

    _name = "scat.menu.rotative"

    name = fields.Char("Nombre", required=True,
                       states={'done': [('readonly', False)]})
    line_ids = fields.One2many("scat.menu.rotative.line", "rotative_id",
                               u"Menús",
                               states={'done': [('readonly', False)]})
    last_created_menu_id = fields.Many2one('scat.menu', u"Últ. menú",
                                           compute="_get_last_menu_data")
    last_created_menu_sequence = fields.Integer(u"Últ. secuencia menú",
                                                compute="_get_last_menu_data")
    start_date = fields.Date("Fecha de inicio", required=True,
                             states={'done': [('readonly', False)]})
    end_date = fields.Date("Fecha de fin",
                           states={'done': [('readonly', False)]})
    state = fields.Selection([('draft', 'Borrador'), ('open', 'En progreso'),
                              ('done', 'Finalizado')], "Estado", required=True,
                             readonly=True, default="draft")

    @api.multi
    def action_open(self):
        self.state = 'open'

    @api.multi
    def action_done(self):
        self.state = 'done'

    @api.multi
    def _get_last_menu_data(self):
        for rotative in self:
            last_menu = self.env['scat.menu'].\
                search([('rotative_line_id', 'in',
                         self.line_ids.ids)], limit=1)
            if last_menu:
                rotative.last_created_menu_id = last_menu.id
                rotative.last_created_menu_sequence = \
                    last_menu.rotative_line_id.sequence

    @api.model
    def _generate_menus(self):
        def next_sequence():
            line = self.env['scat.menu.rotative.line'].\
                search([('sequence', '>', last_sequence),
                        ('rotative_id', '=', rotative.id)], limit=1)
            if line:
                return line
            else:
                line = self.env['scat.menu.rotative.line'].\
                    search([('rotative_id', '=', rotative.id)], limit=1)
                return line

        today = datetime.now()
        next_month = today + relativedelta(months=1)
        rotatives = self.search([('state', '=', 'open'),
                                 ('start_date', '<=',
                                  next_month.strftime("%Y-%m-%d")),
                                 '|', ('end_date', '=', False),
                                 ('end_date', '>=',
                                  today.strftime("%Y-%m-%d"))])
        for rotative in rotatives:
            if rotative.last_created_menu_id:
                last_date = rotative.last_created_menu_id.date
                last_sequence = rotative.last_created_menu_sequence
            else:
                last_date = (datetime.strptime(rotative.start_date,
                                               '%Y-%m-%d') -
                             relativedelta(days=1)).strftime("%Y-%m-%d")
                last_sequence = 0
            final_date = next_month.strftime("%Y-%m-%d")
            if rotative.end_date and final_date > rotative.end_date:
                final_date = rotative.end_date
            while last_date < final_date:
                next_line = next_sequence()
                last_sequence = next_line.sequence
                last_date = (datetime.strptime(last_date, '%Y-%m-%d') +
                             relativedelta(days=1)).strftime("%Y-%m-%d")
                menu = self.env['scat.menu'].\
                    create({'name': u"[%s] %s" % (next_line.rotative_id.name,
                                                  next_line.menu_id.name),
                            'date': last_date,
                            'menu_config_id': next_line.menu_id.id,
                            'state': 'confirmed',
                            'rotative_line_id': next_line.id})
                menu.load_lines()


class ScatMenuRotativeLine(models.Model):

    _name = "scat.menu.rotative.line"
    _order = "sequence asc"

    menu_id = fields.Many2one('scat.menu.config', "Menú", required=True,
                              domain=[('state', '=', 'open')])
    sequence = fields.Integer("Secuencia", required=True, default=1)
    rotative_id = fields.Many2one('scat.menu.rotative', 'Rotativo')

    _sql_constraints = [('rotative_seq_unique',
                         'UNIQUE(rotative_id, sequence)',
                         "Las secuencias no pueden repetirse")]

    @api.multi
    def open_menu_history(self):
        self.ensure_one()
        action = self.env.ref('scat_menu.scat_menu_act').read()[0]
        action['domain'] = [('rotative_line_id', '=', self.id)]
        return action

    @api.model
    def default_get(self, fields=None):
        defaults = super(ScatMenuRotativeLine, self).default_get(fields)
        sequence = 0
        if self.env.context.get('line_ids'):
            for rec in self.env.context['line_ids']:
                if rec[1]:
                    rec_o = self.browse(rec[1])
                    if rec_o.sequence > sequence:
                        sequence = rec_o.sequence
                elif rec[2].get('sequence'):
                    if rec[2]['sequence'] > sequence:
                        sequence = rec[2]['sequence']
            defaults['sequence'] = sequence + 1
        return defaults


class ScatMenu(models.Model):

    _name = "scat.menu"
    _order = "date desc"

    name = fields.Char("Nombre", required=True)
    date = fields.Date("Fecha", required=True)
    menu_config_id = fields.Many2one('scat.menu.config', 'Config.',
                                     required=True)
    state = fields.Selection([('draft', 'Borrador'),
                              ('confirmed', 'Confirmado')], "Estado",
                             readonly=True, required=True, default="draft")
    menu_line_ids = fields.One2many("scat.menu.line", "menu_id", u"Menús")
    rotative_line_id = fields.Many2one('scat.menu.rotative.line', "Rotativo")

    @api.multi
    def action_confirm(self):
        self.state = "confirmed"

    @api.multi
    def load_lines(self):
        for menu in self:
            lines = self.env['scat.menu.config.line'].\
                search([('menu_config_id', '=', menu.menu_config_id.id)])
            lines_data = lines.read([], load='_classic_write')
            for dt in lines_data:
                del dt['id']
                del dt['menu_config_id']
                dt['menu_id'] = menu.id
                self.env['scat.menu.line'].create(dt)

    @api.multi
    def create_prod(self, warehouse, qty, mtype):
        picking_type = self.env['stock.picking.type'].\
            search([('code', '=', 'mrp_operation'),
                    ('warehouse_id', '=', warehouse.id)], limit=1)
        for menu in self:
            for line in menu.menu_line_ids.\
                    filtered(lambda x: mtype in x.mtype_ids and
                             x.product_id.bom_ids):
                if not line.product_id:
                    raise exceptions.Warning(u"Todas las lineas del menú %s "
                                             u"deben de tener producto "
                                             u"asociado." % menu.name)
                prod = self.env['mrp.production'].\
                    create({'menu_line_id': line.id,
                            'product_id': line.product_id.id,
                            'product_qty': qty,
                            'product_uom_id': line.product_id.uom_id.id,
                            'picking_type_id': picking_type.id,
                            'location_src_id':
                            picking_type.default_location_src_id.id,
                            'location_dest_id':
                            picking_type.default_location_dest_id.id,
                            'date_planned_start':
                            fields.Date.from_string(menu.date) -
                            relativedelta(days=1),
                            'date_planned_finished': menu.date,
                            'bom_id': line.product_id.bom_ids[0].id})
                if prod.availability != 'none':
                    prod.action_assign()


class ScatMenuLine(models.Model):

    _inherit = "scat.menu.config.line"
    _name = "scat.menu.line"

    menu_id = fields.Many2one("scat.menu", u"Menú")

    @api.constrains('mode', 'mtype_ids')
    def _check_mode_mtype(self):
        for line in self:
            if line.menu_id:
                for mtype in line.mtype_ids:
                    res = self.search([('menu_id', '=',
                                        line.menu_id.id),
                                       ('id', '!=', line.id),
                                       ('mode', '=', line.mode),
                                       ('mtype_ids', 'in', [mtype.id])])
                    if res:
                        raise exceptions.\
                            ValidationError(u"No se puede repetir el tipo de "
                                            u"menú para el mismo momento")