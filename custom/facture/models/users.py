# -*- coding: utf-8 -*-
from odoo import api, fields, models

class users(models.Model):
    _name = 'facture.users'
    # name = fields.Char("Users")
    #
    user_id = fields.Many2one('res.users','Current User', default=lambda self: self.env.uid)
    def action_open_user(self):
        return {
            'name': 'User information',
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'res_model': 'res.users',
            'domain': [('id', '=', int(self.user_id))]
        }




