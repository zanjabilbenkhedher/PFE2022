# -*- coding: utf-8 -*-
from odoo import api, fields, models

class users(models.Model):
    _name = 'facture.users'
    name = fields.Char("Users")

    user_id = fields.Many2one('res.users','Current User', default=lambda self: self.env.uid)


