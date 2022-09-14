from odoo import api, fields, models


class PengambilanMobil(models.Model):
    _name = "efulrental.pengambilan"
    _description = "Pengambilan Mobil"

    renter_name = fields.Many2one("efulrental.booking", string="Nama Penyewa")
    renter_email = fields.Char(string="Email")
    renter_phone = fields.Char(string="Nomor Telepon")
    renter_age = fields.Integer(string="Umur")
    renter_city = fields.Selection(string='Kota', selection=[('jakarta', 'Jakarta'), ('bandung', 'Bandung'),
                                                      ('sukabumi', 'Sukabumi'), ('bogor', 'Bogor'),
                                                      ('bekasi', 'Bekasi'),('cimahi', 'Cimahi'),
                                                      ('garut', 'Garut'),('depok', 'Depok'),
                                                      ('tasikmalaya', 'Tasikmalaya'),('cirebon', 'Cirebon')])
    start_dt1 = fields.Datetime(string="Tanggal Pengambilan Mobil")
    end_date1 = fields.Date(string="Tanggal Pengembalian Mobil")
    car2 = fields.Many2one("efulrental.stokmobil", string="Mobil")
    fair = fields.Integer(string="fair", help="Total Pembayaran tanpa tax")
    time_slot = fields.Many2one("efulrental.slot", string="Slot Pengambilan Mobil")


    @api.onchange('renter_name')
    def pengambilan_mobil_populate(self):
        for rec in self:
            self.renter_email = rec.renter_name.email_penyewa
            self.renter_city = rec.renter_name.kota_penyewa
            self.renter_phone = rec.renter_name.notelp_penyewa
            self.renter_age = rec.renter_name.umur_penyewa
            self.fair = rec.renter_name.total_cost
            self.start_dt1 = rec.renter_name.ride_start_dt
            self.time_slot = rec.renter_name.checkout_time_slots
            self.end_date1 = rec.renter_name.ride_end_date
            self.car2 = rec.renter_name.car1
            self.env['efulrental.penyewabooking'].search([('booking_id','=',rec.id)])

class SlotPengambilan(models.Model):
    _name = "efulrental.slot"
    _rec_name = "time_slots"
    _description = "Stok Pengambilan Mobil"

    time_slots = fields.Char(string="Slot Waktu Pengambilan")