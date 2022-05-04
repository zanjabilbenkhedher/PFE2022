from odoo import api, fields, models

class InvoiceSettings(models.TransientModel):
    _inherit = "res.config.settings"
    pourcentage =fields.Float(string='Pourcentage')

    def set_values(self):
        res=super(InvoiceSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('facture.pourcentage', self.pourcentage)
        return res

    @api.model
    def get_values(self):
        res = super(InvoiceSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        pourcentages =float(ICPSudo.get_param('facture.pourcentage'))

        res.update(
            pourcentage=pourcentages

        )
        return res