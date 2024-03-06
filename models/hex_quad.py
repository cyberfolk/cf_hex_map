# -*- coding: utf-8 -*-

from odoo import api, fields, models
from ..utility.odoo_to_json import obj_odoo_to_json
from ..utility.costant import BORDERS_MAP


class Quadrant(models.Model):
    _name = "hex.quad"
    _inherit = ['hex.mixin']
    _description = "Quadrant, contains Hexagons."

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

    hook_widget = fields.Char(
        string="hook_widget",
        help="Usato solamente per agganciare il widget del quadrante."
    )

    border_N = fields.Many2one(
        comodel_name='hex.quad',
        string="N",
        help="Confine Nord"
    )

    border_NE = fields.Many2one(
        comodel_name='hex.quad',
        string="NE",
        help="Confine Nord-Est"
    )

    border_SE = fields.Many2one(
        comodel_name='hex.quad',
        string="SE",
        help="Confine Sud-Est"
    )

    border_S = fields.Many2one(
        comodel_name='hex.quad',
        string="S",
        help="Confine Sud"
    )

    border_SW = fields.Many2one(
        comodel_name='hex.quad',
        string="SW",
        help="Confine Sud-Ovest"
    )

    border_NW = fields.Many2one(
        comodel_name='hex.quad',
        string="NW",
        help="Confine Nord-Ovest"
    )

    @api.model
    def get_json_quad(self, quad_id):
        """Metodo richiamato dal orm di quad.js
            :param quad_id: Id quadrante.
            :return: Json del quadrante."""
        self_quad = self.env['hex.quad'].browse(quad_id)[0]
        json_quad = obj_odoo_to_json(self_quad)
        return json_quad

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

    def set_hexs_borders(self):
        """Metodo per impostare i bordi degli Esagoni. Gestire casistiche:
             1 - Esagoni mancanti,
             2 - Esagoni di confine """
        for hex in self.hex_ids:
            borders = BORDERS_MAP[hex.index]
            hex.border_N = next((x for x in self.hex_ids if x['index'] == borders[0]), None)
            hex.border_NE = next((x for x in self.hex_ids if x['index'] == borders[1]), None)
            hex.border_SE = next((x for x in self.hex_ids if x['index'] == borders[2]), None)
            hex.border_S = next((x for x in self.hex_ids if x['index'] == borders[3]), None)
            hex.border_SW = next((x for x in self.hex_ids if x['index'] == borders[4]), None)
            hex.border_NW = next((x for x in self.hex_ids if x['index'] == borders[5]), None)