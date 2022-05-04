# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ModelActivity(models.Model):
    _name = 'facture.model.activity'
    name = fields.Char("Name")
    invoicemodel_id = fields.Many2one("facture.fact")
    model_id=fields.Many2one("ir.model")
    res_id=fields.Char("Id")
    compare = fields.Float("Compare")
    showImage = fields.Image("Show Invoice")
    stateActivity =[
        ('draft','Draft'),
        ('progress','Progress'),
        ('validate','Validate'),
        ('reject','Reject'),
    ]
    state = fields.Selection(stateActivity,default="draft")
    last_date = fields.Date(string='last_create', default=fields.Date.today(), required=True, copy=False)