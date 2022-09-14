from odoo import api, fields, models
from odoo.exceptions import ValidationError
from collections import namedtuple
from datetime import datetime


class BookingMobil(models.Model):
    _name = "efulrental.booking"
    _rec_name = "nama_penyewa"
    _description = "Booking Sewa Mobil"

    nama_penyewa = fields.Many2one("efulrental.penyewa", string="Nama Penyewa", domain=[("status", "=", "submitted")])
    email_penyewa = fields.Char(string="Email")
    notelp_penyewa = fields.Char(string="Nomor Telepon")
    umur_penyewa = fields.Integer(string="Umur Penyewa")
    driver_req = fields.Boolean(string="Dengan Supir",
                                help="Ceklis apabila membutuhkan supir akan kena bayaran 1500/day.", default=True)
    ride_start_dt = fields.Date(string="Tanggal dimulai", default=fields.Datetime.today(),
                                help="Masukkan Tanggal Mulai")
    ride_end_date = fields.Date(string="Tanggal Selesai Sewa", help="Masukkan Tanggal Akhir Sewa Mobil")
    checkout_time_slots = fields.Many2one("efulrental.slot", string="Slot Waktu Pembayaran")
    car1 = fields.Many2one("efulrental.stokmobil", string="Mobil", domain=[("car_status", "=", "dalam_garasi")])
    days_interval = fields.Integer(string="Sewa Berapa Hari?", store=True)
    cost_per_day = fields.Integer(string="Bayaran Perhari")
    cost_per_day1 = fields.Integer(string="Bayaran Perharinya")
    total_cost = fields.Integer(string="Total Pembayaran", store=True)
    book_status = fields.Selection(
        [('draft', 'Draft'), ('submitted', 'Submitted'), ('cancel', 'Cancel')], default='draft')
    ride_booked = fields.Boolean(string="Booked")
    alamatlengkap_penyewa = fields.Text(string="Alamat Lengkap Penyewa", help="Masukkan Alamat Lengkap!")
    kota_penyewa = fields.Selection(string='Kota', selection=[('jakarta', 'Jakarta'), ('bandung', 'Bandung'),
                                                      ('sukabumi', 'sukabumi'), ('bogor', 'Bogor'),
                                                      ('bekasi', 'Bekasi'),('cimahi', 'Cimahi'),
                                                      ('garut', 'Garut'),('depok', 'Depok'),
                                                      ('tasikmalaya', 'Tasikmalaya'),('cirebon', 'Cirebon')])
    car_brand = fields.Selection(
        [('Maruti Suzuki', 'Maruti Suzuki'), ('Honda', 'Honda'), ('Hyundai', 'Hyundai'), ('Skoda', 'Skoda'),
         ('Ford', "Ford"), ('Tata', 'Tata'), ('Toyota', 'Toyota'), ('Renault', 'Renault'), ('Mahindra', 'Mahindra'),
         ('Kia', 'Kia')])
    tipe_mobil1 = fields.Selection([('hatchback', 'Hatchback'), ('sedan', 'Sedan'), ('suv', 'SUV'), ('muv', 'MUV')],
                                 string="Tipe Mobil")
    tax_on_product = fields.Integer(string="tax", store=True)
    price_after_tax = fields.Integer(string="setelah dikasih tax", store=True)
    date_today = fields.Date(string="Tanggal hari ini", default=fields.Datetime.today())
    booking_count = fields.Integer(string="Total pembayaran booking", compute='get_booking_count')

    @api.onchange('nama_penyewa', 'car1')
    def pengambilan_mobil_populate(self):
        for rec in self:
            self.email_penyewa = rec.nama_penyewa.email
            self.notelp_penyewa = rec.nama_penyewa.notelp
            self.umur_penyewa = rec.nama_penyewa.umur
            self.alamatlengkap_penyewa = rec.nama_penyewa.alamatlengkap
            self.kota_penyewa = rec.nama_penyewa.kota
            self.cost_per_day = rec.car1.harga_sewa
            self.cost_per_day1 = rec.car1.harga_sewa
            self.car_brand = rec.car1.brand
            self.tipe_mobil1 = rec.car1.tipe_mobil

            print("customer email >>>>>>>>>>>>>>", self.email_penyewa)
            print("customer phone >>>>>>>>>>>>>>", self.notelp_penyewa)
            print("customer age >>>>>>>>>>>>>>", self.umur_penyewa)
            print("cost per day >>>>>>>>>>>>>", self.cost_per_day)

    @api.onchange('ride_start_dt', 'ride_end_date')
    def _date_difference(self):
        if self.ride_start_dt and self.ride_end_date:
            if self.ride_start_dt > self.ride_end_date:
                raise ValidationError('Date_in should not greater than Date_out.')
            # self.days_interval = 0
            if self.ride_start_dt < self.ride_end_date:
                day_calc = (self.ride_end_date - self.ride_start_dt).days
                self.days_interval = day_calc

    @api.onchange('days_interval', 'total_cost', 'cost_per_day1', 'cost_per_day', 'driver_req', 'car1')
    def _calculate_total(self):
        if self.days_interval == 0:
            if self.driver_req:
                self.cost_per_day1 = self.cost_per_day + 1500
                self.total_cost = self.cost_per_day1
                self.pengambilan_mobil_populate()
            else:
                self.cost_per_day1 = self.cost_per_day
                self.total_cost = self.cost_per_day1
        else:
            if self.driver_req:
                self.cost_per_day1 = self.cost_per_day + 1500
                self.total_cost = self.days_interval * self.cost_per_day1
            else:
                self.cost_per_day1 = self.cost_per_day
                self.total_cost = self.days_interval * self.cost_per_day1

        self.pengambilan_mobil_populate()

        self.tax_on_product = self.total_cost * 0.15
        self.price_after_tax = self.total_cost + self.tax_on_product
    @api.constrains('car1')
    def check_availability(self):
        mobil_sama = self.env['efulrental.booking'].sudo().search([('id', '!=', self.id)])
        print("whole record >>>>>>>>>>>>>>>", mobil_sama)
        for rec in mobil_sama:
            print("rec.car1rec.car1rec.car1", rec.car1)
            if rec.car1 == self.car1:
                date1_start = rec.ride_start_dt
                date1_end = rec.ride_end_date
                Range = namedtuple('Range', ['start', 'end'])
                r1 = Range(start=date1_start, end=date1_end)
                r2 = Range(start=self.ride_start_dt, end=self.ride_end_date)
                latest_start = max(r1.start, r2.start)
                earliest_end = min(r1.end, r2.end)
                delta = (earliest_end - latest_start).days + 1
                print("delta >>>>>>>>>>>", delta, end="\n")
                overlap = max(0, delta)
                print("overlap >>>>>>>>>>>", overlap, end="\n")
                if overlap != 0:
                    raise ValidationError("Mobil Tidak Tersedia Silahkan Pilih Mobil Lain")

    def submit_action(self):
        self.book_status = "submitted"

    def action_cancel(self):
        self.book_status = 'cancel'

    def action_draft(self):
        self.book_status = 'draft'

    @api.model
    def create(self, values):
        print('create values >>', values)
        values['ride_booked'] = True
        values['book_status'] = 'submitted'
        rtn = super(BookingMobil, self).create(values)
        print('return value of create is >>', rtn)
        return rtn

    def write(self, values):
        print('write values >>', values)
        values['ride_booked'] = True
        rtn = super(BookingMobil, self).write(values)
        print('return value of create is >>', rtn)
        return rtn

    def unlink(self):
        if self.book_status not in ('draft', 'cancel'):
            raise ValidationError("Booking yang di submit tidak bisa dihapus")
        rtn = super(BookingMobil, self).unlink()
        return rtn

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):

        rec = super(BookingMobil, self).read_group(domain, fields, groupby, offset=offset, limit=limit,
                                               orderby=orderby, lazy=lazy)
        if 'umur_penyewa' in fields:
            for lines in rec:
                lines['umur_penyewa'] = False
        return rec

