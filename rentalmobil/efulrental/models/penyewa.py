from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Penyewa(models.Model):
    _name = 'efulrental.penyewa'
    _rec_name = "name"
    _description = 'Informasi Penyewa'

    name = fields.Char(string='Nama', help="ini adalah Nama Penyewa.")
    email = fields.Char(string='Email', help="Email Penyewa")
    notelp = fields.Char(string='No Telpon', help="Masukkan Nomor Kontak yang bisa dihubungi", required=True)
    umur = fields.Integer(string='Umur', default=18, help="Masukkan Umur Kamu")
    kota = fields.Selection(string='Kota', selection=[('jakarta', 'Jakarta'), ('bandung', 'Bandung'),
                                                      ('sukabumi', 'Sukabumi'), ('bogor', 'Bogor'),
                                                      ('bekasi', 'Bekasi'),('cimahi', 'Cimahi'),
                                                      ('garut', 'Garut'),('depok', 'Depok'),
                                                      ('tasikmalaya', 'Tasikmalaya'),('cirebon', 'Cirebon')], required=True)
    alamatlengkap = fields.Text(string='Alamat Lengkap', help="Masukkan Alamat Lengkap")
    status = fields.Selection( selection=[('draft', 'Draft'), ('submitted', 'Submitted'),('cancel', 'Cancel')], default='draft')
    sim = fields.Image(string="Upload SIM",
                         help="Upload SIM kamu", required=True)
    foto = fields.Image(string="Upload Foto",
                         help="Upload Foto kamu", required=True)
    car = fields.Many2one("efulrental.stokmobil", string="Mobil")
    penyewa_booking = fields.One2many("efulrental.penyewabooking", "booking_id", string="Customer Bookings")
    bookings_count = fields.Integer(string="Nomor Booking Penyewa", compute="get_booking_count")

    def get_booking_count(self):
        for rec in self:
            booking_count = self.env['efulrental.booking'].search_count([('nama_penyewa', '=', rec.nama_penyewa)])
            rec.bookings_count = booking_count


    @api.constrains('end_date')
    def _check_end_date(self):
        for record in self:
            if record.end_date < record.start_dt.date():
                raise ValidationError("Pilih Tanggal Selesai Sewa!")

    @api.constrains('notelp')
    def _phone_validation(self):
        for record in self:
            if len(record.notelp) != 12:
                raise ValidationError("Nomor Telepon harus 12 Digit!")
            if not (record.notelp.isnumeric()):
                raise ValidationError("Nomor telepon harus berupa angka!")

    def submit_action(self):
        self.status = "submitted"

    def action_cancel(self):
        self.status = 'cancel'

    def action_draft(self):
        self.status = 'draft'

    def unlink(self):
        try:
            rtn = super(Penyewa, self).unlink()
            return rtn
        except:
            raise ValidationError("Penyewa tidak bisa dihapus!")

    def action_draft(self):
        self.status = 'draft'

    def action_submit(self):
        self.status = 'submitted'

    def action_open_bookings(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Bookings',
            'res_model': 'efulrental.booking',
            'domain': [('cus_name', '=', self.id)],
            'view_mode': 'tree,form',
            'target': 'current',
        }

class PenyewaBooking(models.Model):
    _name = "efulrental.penyewabooking"
    _description = "Penyewa Melakukan Booking"

    bookings = fields.Many2one('efulrental.booking', string="bookings")
    booking_id = fields.Many2one('efulrental.penyewa', string="booking id")

    driver_req1 = fields.Boolean(string="Dengan Sopir?",
                                 help="ceklis ini jika kamu butuh sopir!")
    sequence = fields.Integer(string="Sequence")
    ride_start_dt1 = fields.Date(string="Tanggal Mulai",
                                 help="Masukkan Tanggal Mulai Sewa Mobil")
    ride_end_date1 = fields.Date(string="Tanggal Selesai Sewa", help="Masukkan Tanggal Akhir Sewa Mobil")
    car2 = fields.Many2one("efulrental.stokmobil", string="Mobil")
    @api.onchange('bookings')
    def bookings_populate(self):
        for rec in self:
            self.driver_req1 = rec.bookings.driver_req
            self.ride_start_dt1 = rec.bookings.ride_start_dt
            self.ride_end_date1 = rec.bookings.ride_end_date
            self.car2 = rec.bookings.car1
    
    
    
    
    
