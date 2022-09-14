from odoo import api, fields, models


class StokMobil(models.Model):
    _name = "efulrental.stokmobil"
    _rec_name = "nama_mobil"
    _description = "Stok Mobil"

    nama_mobil = fields.Char(string="Nama Mobil", required=True)
    tipe_mobil = fields.Selection([('hatchback', 'Hatchback'), ('sedan', 'Sedan'), ('suv', 'SUV'), ('muv', 'MUV')],
                                string="Tipe Mobil")
    kursi = fields.Integer(string="Kursi")
    brand = fields.Selection(
        [('Maruti Suzuki', 'Maruti Suzuki'), ('Honda', 'Honda'), ('Hyundai', 'Hyundai'), ('Skoda', 'Skoda'),
         ('Ford', "Ford"), ('Tata', 'Tata'), ('Toyota', 'Toyota'), ('Renault', 'Renault'), ('Mahindra', 'Mahindra'),
         ('Kia', 'Kia')])
    foto3 = fields.Image(string="Photo Mobil")
    harga_sewa = fields.Integer(string="Harga Sewa Perhari")
    car_status = fields.Selection(
        [('dalam_garasi','Dalam Garasi'),('disewa', 'Disewa'), ('dalam_perbaikan', 'Dalam Perbaikan'), ('tidak_tersedia', 'Tidak Tersedia')],
        default='dalam_garasi')
    car_booking_count = fields.Integer(string="Nomor Booking Customer", compute="get_car_booking_count")

    def get_car_booking_count(self):
        for rec in self:
            booking_count = self.env['efulrental.booking'].search_count([('car1', '=', rec.nama_mobil)])
            rec.car_booking_count = booking_count

    def dalam_garasi_action(self):
        self.car_status = 'dalam_garasi'

    def disewa_action(self):
        self.car_status = 'disewa'

    def dalam_perbaikan_action(self):
        self.car_status = 'dalam_perbaikan'

    def action_tidak_tersedia(self):
        self.car_status = 'tidak_tersedia'

    def name_get(self):
        res = []
        for field in self:
            res.append((field.id, '%s %s [%s]' % (field.brand, field.nama_mobil, field.tipe_mobil)))
        return res

    def action_open_car_bookings(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Bookings',
            'res_model': 'efulrental.booking',
            'domain': [('car1', '=', self.id)],
            'view_mode': 'tree,form',
            'target': 'current',
        }
