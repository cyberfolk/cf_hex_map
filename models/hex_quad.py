# -*- coding: utf-8 -*-
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)

from odoo import api, fields, models


class Quadrant(models.Model):
    _name = "hex.quad"
    _description = "Quadrant, contains Hexagons."

    name = fields.Char(
        string='Name',
        store=True,
    )

    code = fields.Char(
        string='Code',
        compute='_compute_code',
    )

    macro_id = fields.Many2one(
        comodel_name='hex.macro',
        string="Macro Area",
    )

    hex_list = fields.Char(
        string="Hex list",
    )

    hex_ids = fields.One2many(
        comodel_name='hex.hex',
        string="Hexes",
        inverse_name='quad_id',
    )

    polygon = fields.Char(
        string='Polygon'
    )

    circle_order = fields.Integer(
        string='Circle Order',
        compute='_compute_circle_order',
    )

    circle_number = fields.Integer(
        string='Circle Number',
        compute='_compute_circle_number',
    )

    index = fields.Integer(
        string='Index',
        help="Il valore di 'index' deve essere compreso tra 1 e 19.",
    )

    color = fields.Char(
        string='Color',
    )


    @api.constrains('index')
    def _check_index(self):
        for record in self:
            if record.index < 1 or record.index > 19:
                raise ValidationError("Il valore di 'index' deve essere compreso tra 1 e 19.")

    @api.depends('index')
    def _compute_code(self):
        for record in self:
            record.code = (chr(ord('A') + record.index - 1))

    @api.constrains('name')
    def check_name(self):
        for record in self:
            if not record.name:
                record.name = record.code

    @api.model_create_multi
    def create(self, vals):
        quads = super(Quadrant, self).create(vals)
        hex_list = eval(vals[0]['hex_list'])
        hex_macro = self.env.ref('cf_hex_map.hex_macro_1')
        for quad in quads:
            quad.check_name()
            quad.macro_id = self.env.ref('cf_hex_map.hex_macro_1')
            for index in hex_list:
                hex_id = self.env['hex.hex'].create({
                    'quad_id': quad.id,
                    'index': index,
                    'color': quad.color,
                })
                hex_id.check_name()
                quad.hex_ids = [(4, hex_id.id)]
            hex_macro.quadrant_ids = [(4, quad.id)]
        return quads

    @api.depends('index')
    def _compute_circle_order(self):
        for record in self:
            if record.index == 1:
                record.circle_order = 0
            elif 2 <= record.index <= 7:
                record.circle_order = 1
            elif 8 <= record.index <= 19:
                record.circle_order = 2
            else:
                record.circle_order = None

    @api.depends('index')
    def _compute_circle_number(self):
        for record in self:
            if record.index == 1:
                record.circle_number = 1
            elif 2 <= record.index <= 7:
                record.circle_number = record.index - 1
            elif 8 <= record.index <= 19:
                record.circle_number = record.index - 7
            else:
                record.circle_number = None
