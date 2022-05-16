# -*- coding: utf-8 -*-
from soupsieve import select

from odoo import api, fields, models, _
import json
import datetime
from odoo.exceptions import ValidationError
import base64
from PIL import Image
from io import BytesIO
class FactureFact(models.Model):
    _name = 'facture.fact'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    fournisseur = fields.Text("Supplier")
    vat = fields.Text("Vat")
    adresse=fields.Text("Adresse")
    billDate=fields.Date("Bill Date")
    dueDate = fields.Date("Due Date")
    iban=fields.Char("IBAN")
    currency=fields.Text("Currence")
    montantT = fields.Float("Total")
    lines=fields.Char("Lines")
    detaille = fields.Text("detaille image")
    imageCode = fields.Text()
    prescription = fields.Text(string="Prescription")
    OtherInfo = fields.Text(string="info")
    detail_ids = fields.One2many('facture.details', 'facture_id')
    name_seq = fields.Char(string='Invoice Num',
                           required=True,
                           copy=False, readonly=True, index=True
                           , default=lambda self: _('New'))
    reference = fields.Text("Reference")

    _rec_name = "name_seq"
    model_id = fields.Many2one(comodel_name='ir.model')
    child_ids = fields.One2many('facture.fact', 'parent_id')
    parent_id= fields.Many2one('facture.fact')
    last_date = fields.Date(string='last_create', default=fields.Date.today(), required=True, copy=False)
    codeZoning = fields.Image("Invoice Model")
    test = fields.Text("test")

    def displayFacture(self):
        for i in self:
            i.display_facture_image = i.imageCode

    display_facture_image = fields.Image(compute=displayFacture)

    @api.onchange('Facture_image')
    def _onchange_field(self):
        for i in self:
            i.display_facture_image = i.imageCode

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
                            'champ1':data[x]['champ1'],
                            'champ2': data[x]['champ2'],
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
        # if not "imageCode" in vals:
        #     raise ValidationError(_(
        #         'You can not modify the field "Use Documents?" if there are validated invoices in this journal!'))
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('facture.fact.sequence') or _('New')
        result = super(FactureFact, self).create(vals)
        # self.send_Notification('test_create', result.create_uid.id, self._name, result.id, note='<i> test odoo</i>')
        return result

    @api.model
    def createDetails(self,data=[],model_id=False,deleteListe=[],id=False):
        print(data)
        print(id)
        # if self.detaille:
        tab = []
        modelId=False
        if id:
            modelId=self.browse(int(id))
        if model_id:
            self.browse(int(id)).write({'model_id':model_id})
        if len(deleteListe)>0:
            self.env['facture.details'].browse(deleteListe).unlink()
        if data and id:
            for x in range(0, len(data)):
                # if not self.checkDetails(data[x]):
                ligne={
                            'x': data[x]['x'],
                            'y': data[x]['y'],
                            'height': data[x]['height'],
                            'width': data[x]['width'],
                            'champ1': data[x]['champ1'],
                            'champ2': data[x]['champ2'],
                            'isTable':data[x]['isTable'],
                            'field_id':data[x]['field_id'],
                            'facture_id':modelId.id,

                            # 'model_id': self.model_id.id
                        }

                if not data[x]['id']:
                    if data[x]['isTable']:
                        res= self.create({
                            'parent_id': modelId.id,
                            'imageCode': self.env['facture.details']._cropImage(modelId.imageCode,
                                                                                (float(data[x]['x']), float(data[x]['y']),
                                                                                 float(data[x]['width']) + float(data[x]['x']),
                                                                                 float(data[x]['height']) + float(data[x]['y'])))
                        })
                        ligne["tableModel_id"]=res.id
                    tab.append([
                        0, 0, ligne
                    ])
                else:
                    self.env['facture.details'].browse(int(data[x]['id'])).write(ligne)
            if len(tab) > 0:
                self.browse(int(id)).write({'detail_ids': tab})



        return data

    def action_open_facture(self):
        print("Test")

    @api.model
    def getModel(self):
        model = self.env['ir.model'].search([])
        liste=[]
        for m in model:
            liste.append({
                'id':m.id,
                'name':m.name,
            })


        return  liste


    @api.model
    def getField(self,model_id):
        # model=self.env['ir.model'].search([('name','=',model_id)])
        field = self.env['ir.model.fields'].search([('model_id','=',model_id)])
        liste = []
        for f in field:
            liste.append({
                'id': f.id,
                'name': f.name,
            })

        print(liste)
        return liste

    @api.model
    def getModelId(self,id):
        if not id:
            ICPSudo = self.env['ir.config_parameter'].sudo()
            defaultModelFact = ICPSudo.get_param('facture.defaultModelFact')
            return int(defaultModelFact) if defaultModelFact else False
        return self.browse(id).model_id.id


    def send_Notification(self,summary,user_id,res_model,res_id,note=False):
        self.env['mail.activity'].sudo().create({
            'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
            'date_deadline': datetime.datetime.now().date() ,
            'summary':summary,
            'user_id':user_id,
            'note':note,
            'res_model':res_model ,
            'res_model_id':self.env['ir.model'].sudo().search([('model', '=' , res_model)], limit=1).id,
            'res_id': res_id,
        })

        return True

    # @api.constrains('imageCode')
    # def check_imageCode(self):
    #     for rec in self:
    #         if not rec.imageCode:
    #             raise ValidationError(_(
    #                 'You can not modify the field "Use Documents?" if there are validated invoices in this journal!'))

