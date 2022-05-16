# -*- coding: utf-8 -*-
from soupsieve import select

from odoo import api, fields, models, _

class UserProfile(models.Model):
    _name = 'user.profile'
    user = fields.Text("Username")
    password = fields.Text("Password")

    # @api.one
    # def _get_current_login_user(self):
    #
    #     user_obj = self.env['res.users'].search([])
    #
    #     for user_login in user_obj:
    #
    #         current_login = self.env.user
    #
    #         if user_login == current_login:
    #
    #             self.processing_staff = current_login
    #
    #     return


