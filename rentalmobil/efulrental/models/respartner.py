from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'
    _description = 'New Description'
    
    is_mediapartner = fields.Boolean(string='Is Media Partner')
    is_kolpartner = fields.Boolean(string='Is KOL Partner')