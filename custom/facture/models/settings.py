from odoo import api, fields, models

class InvoiceSettings(models.TransientModel):
    _inherit = "res.config.settings"
    pourcentage =fields.Float(string='Pourcentage')
    defaultModelFact= fields.Many2one('ir.model')

    def set_values(self):
        res=super(InvoiceSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('facture.pourcentage', self.pourcentage )
        self.env['ir.config_parameter'].set_param('facture.defaultModelFact', self.defaultModelFact.id)
        return res

    @api.model
    def get_values(self):
        res = super(InvoiceSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        pourcentages =float(ICPSudo.get_param('facture.pourcentage'))
        defaultModelFact =ICPSudo.get_param('facture.defaultModelFact')

        res.update(
            pourcentage=pourcentages,
            defaultModelFact=int(defaultModelFact) if defaultModelFact else False

        )
        return res