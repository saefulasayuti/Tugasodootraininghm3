from odoo import api, fields, models
from odoo.exceptions import ValidationError

class Staff(models.Model):
    _name = "efulrental.staff"
    _rec_name = "name"
    _description = "Data Staff"

    name = fields.Char(string='Nama', help="isi nama lengkap kamu", required=True)
    email = fields.Char(string='Email')
    notelp = fields.Char(string='Nomor Telpon', help="masukan nomor telpon", required=True)
    umur = fields.Integer(string='Umur')
    kota = fields.Selection(string='Kota', selection=[('jakarta', 'Jakarta'), ('bandung', 'Bandung'),
                                                      ('sukabumi', 'sukabumi'), ('bogor', 'Bogor'),
                                                      ('bekasi', 'Bekasi'),('cimahi', 'Cimahi'),
                                                      ('garut', 'Garut'),('depok', 'Depok'),
                                                      ('tasikmalaya', 'Tasikmalaya'),('cirebon', 'Cirebon')], required=True)
    role = fields.Selection(
        [('manager', 'Manager'), ('driver', 'Driver'), ('accounting', 'Accounting'), ('mechanic', 'Mechanic')],
        string="Role",
        required=True, help="pilih role kamu")
    sim = fields.Image(string="Upload SIM",
                         help="Upload SIM kamu")
    foto2 = fields.Image(string="Upload Foto",
                         help="Upload Foto kamu")
    status = fields.Selection(
        [('cancel', 'Cancel'), ('draft', 'Draft'), ('submitted', 'Submitted'), ('approved', 'Approved')],
        default='draft')

    @api.model
    def create(self, values):
        if values['sim']:
            values['status'] = 'submitted'
        else:
            raise ValidationError("Profil tidak diveritifikasi jika kamu tidak mengirim sim")
        print(">>>>sim>>>>", values['sim'])
        rtn = super(Staff, self).create(values)
        print('return value of create is >>', rtn)
        return rtn

    def write(self, values):
        if values['sim']:
            values['status'] = 'submitted'
        rtn = super(Staff, self).write(values)
        return rtn

    @api.constrains('notelp')
    def _phone_validation(self):
        for record in self:
            if len(record.notelp) != 12:
                raise ValidationError("Nomor Telepon Harus 12 Digit")
            if not (record.notelp.isnumeric()):
                raise ValidationError("Nomor Telepon Harus Angka!")

    def submit_action(self):
        self.status = "submitted"

    def action_cancel(self):
        self.status = 'cancel'

    def action_draft(self):
        self.status = 'draft'
      

class BrandAmbassador(models.Model):
    _name = 'efulrental.brandambassador'
    _inherit = 'efulrental.staff'
    _description = 'Brand Ambassador'

    id_ambassador = fields.Char(string='ID Staff')
    jenis_kelamin = fields.Selection(string='Jenis Kelamin', selection=[('lakilaki', 'Laki Laki'), ('perempuan', 'Perempuan'),])
    
    
    
    
    