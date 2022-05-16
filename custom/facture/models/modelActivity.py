# -*- coding: utf-8 -*-
from odoo import api, fields, models,_
import datetime
from odoo.exceptions import ValidationError
class ModelActivity(models.Model):
    _name = 'facture.model.activity'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    invoicemodel_id = fields.Many2one("facture.fact",string="Invoice Model")
    model_id=fields.Many2one("ir.model")
    res_id=fields.Char("Id")
    compare = fields.Float("% Comparison")
    showImage = fields.Image(string="Model")
    stateActivity =[
        ('draft','Draft'),
        ('progress','Progress'),
        ('validate','Validate'),
        ('reject','Reject'),
    ]
    state = fields.Selection(stateActivity,default="draft")
    last_date = fields.Date(string='last_create', default=fields.Date.today(), required=True, copy=False)
    name_seq2 = fields.Char(string='Order Reference',
                            required=True,
                            copy=False, readonly=True, index=True
                            , default=lambda self: _('New'))

    _rec_name = "name_seq2"



    @api.model
    def create(self, vals):
        if vals.get('name_seq2', _('New')) == _('New'):
            vals['name_seq2'] = self.env['ir.sequence'].next_by_code('facture.model.activity.sequence') or _('New')
        result = super(ModelActivity, self).create(vals)
        return result

    def action_open_model(self):
        return {
            # 'name': _('Checks to Print'),
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'res_model': self.model_id.model,
            'domain' : [('id', '=',int(self.res_id))]
        }

    def action_draft(self):
        self.state='draft'
        users = self.env.ref('facture.group_facture_modelManager').users
        for user in users:
            self.send_Notification("draft", user.id, self._name, self.id, "<li>test</li>")

    def action_progress(self):
        self.state='progress'
        users = self.env.ref('facture.group_facture_modelManager').users
        for user in users:
            self.send_Notification("progress",user.id,self._name,self.id,"<li>Model in progress</li>")


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

    def action_validate(self):
        invoice=self.env['create.facture.wizard'].create({
            'uploadedFacture':self.showImage,
        }).read_by_model(self.invoicemodel_id)

        if not invoice:
            raise ValidationError("model invalid")
        else:
            self.write({
                'state':'validate',
                'model_id':self.env['ir.model'].sudo().search([('model', "=", invoice._name)] ,limit=1),
                'res_id':invoice.id
            })

    def action_reject(self):
        res = self.env[self.model_id.model].browse(int(self.res_id))
        if res:
            res.unlink()

        self.write({
            'state':'reject',
            'model_id':False,
            'res_id':False
        })



    def show_alert(self):
        return{
            'type':'ir.actions.window',
            'tag': 'display_notification',
            'params': {
                'title': _('Warning!'),
                'message':'This model will be rejected',
                'sticky':True,
            }
        }
