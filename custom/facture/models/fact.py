# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import json


class FactureFact(models.Model):
    _name = 'facture.fact'
    fournisseur = fields.Char("Supplier")
    vat = fields.Text("Vat")
    adresse=fields.Text("Adresse")
    billDate=fields.Date("Bill Date")
    dueDate = fields.Date("Due Date")
    iban=fields.Text("IBAN")
    currency=fields.Text("Currence")
    montantT = fields.Float("Total")
    reference = fields.Char("Reference")
    lines=fields.Text("Lines")
    detaille = fields.Text("detaille image")
    imageCode = fields.Text()
    prescription = fields.Text(string="Prescription")
    OtherInfo = fields.Text(string="info")
    detail_ids = fields.One2many('facture.details', 'facture_id')
    name_seq = fields.Char(string='Order Reference',
                           required=True,
                           copy=False, readonly=True, index=True
                           , default=lambda self: _('New'))

    _rec_name = "name_seq"
    name_facture = fields.Char("name")
    model_id = fields.Many2one(comodel_name='ir.model')


    codeZoning = fields.Image("code zoning")

    test = fields.Text("test")


    # @api.onchange('detaille')
    def onchangeDetaille(self):
        if self.detaille:
            data = json.loads(self.detaille)
            tab = []
            for x in range(0, len(data)):
                if not self.checkDetails(data[x]):
                    tab.append([
                        0, 0, {
                            'x': data[x]['x'],
                            'y': data[x]['y'],
                            'height': data[x]['height'],
                            'width': data[x]['width'],
                            'model_id': self.model_id.id
                        }
                    ])
            if len(tab)>0:
                self.write({'detail_ids' : tab})


    def checkDetails(self,data):
        for i in self.detail_ids:
            if i.x == data['x'] and i.y == data['y'] and i.width == data['width'] and i.height == data['height']:
                return True
        return False

    @api.onchange('imageCode')
    def onchangeImage(self):
        self.imageCode=self.imageCode



    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('facture.fact.sequence') or _('New')
        result = super(FactureFact, self).create(vals)
        return result

    @api.model
    def createDetails(self,data,id):
        print(data)
        print(id)
        # if self.detaille:
        tab = []
        for x in range(0, len(data)):
                # if not self.checkDetails(data[x]):
            tab.append([
                        0, 0, {
                            'x': data[x]['x'],
                            'y': data[x]['y'],
                            'height': data[x]['height'],
                            'width': data[x]['width'],
                            # 'model_id': self.model_id.id
                        }
                    ])
        if len(tab)>0:
            self.browse(int(id)).write({'detail_ids' : tab})

        return True

    def actio