from odoo import api, fields, models
from odoo.exceptions import ValidationError
from collections import namedtuple


class BookRideWizard(models.Model):
    _name = "efulrental.bookingwizard"
    _description = "Booking"

    name = fields.Many2one("efulrental.booking", string="Nama Penyewa")
    nama_penyewa = fields.Many2one("efulrental.penyewa", string="Nama Penyewanya", domain=[("status", "=", "submitted")])
    email_penyewa = fields.Char(string="Email")
    notelp_penyewa = fields.Char(string="Nomor Telepon")
    umur_penyewa = fields.Integer(string="Umur Penyewa")
    driver_req = fields.Boolean(string="Dengan Sopir ?",
                                help="Ceklis disini apabila kamu mau memakai sopir kena bayaran 1500/hari")
    ride_start_dt = fields.Date(string="Tanggal Mulai", default=fields.Datetime.today(),
                                help="Tanggal Selesai Sewa")
    ride_end_date = fields.Date(string="Tanggal Selesai", default=fields.Date.today(), help="Masukkan Tanggal Selesai Sewa")
    checkout_time_slots = fields.Many2one("efulrental.slot", string="Slot Waktu Pengambilan")
    car1 = fields.Many2one("efulrental.stokmobil", string="Mobil", domain=[("car_status", "=", "dalam_garasi")])
    days_interval = fields.Integer(string="Berapa Hari?", store=True)
    cost_per_day = fields.Integer(string="Bayaran Perhari", store=True)
    total_cost = fields.Integer(string="Total Pembayaran", store=True)
    book_status = fields.Selection(
        [('draft', 'Draft'), ('submitted', 'Submitted'), ('cancel', 'Cancel')], default='draft')
    ride_booked = fields.Boolean(string="Booked")
    kota_penyewa = fields.Selection(string='Kota', selection=[('jakarta', 'Jakarta'), ('bandung', 'Bandung'),
                                                      ('sukabumi', 'sukabumi'), ('bogor', 'Bogor'),
                                                      ('bekasi', 'Bekasi'),('cimahi', 'Cimahi'),
                                                      ('garut', 'Garut'),('depok', 'Depok'),
                                                      ('tasikmalaya', 'Tasikmalaya'),('cirebon', 'Cirebon')])

    @api.onchange('nama_penyewa', 'car1')
    def pengambilan_mobil_populate(self):
        for rec in self:
            self.email_penyewa = rec.nama_penyewa.email
            self.notelp_penyewa = rec.nama_penyewa.notelp
            self.umur_penyewa = rec.nama_penyewa.umur
            self.kota_penyewa = rec.nama_penyewa.kota
            self.cost_per_day = rec.car1.harga_sewa
            print("customer email >>>>>>>>>>>>>>", self.email_penyewa)
            print("customer phone >>>>>>>>>>>>>>", self.notelp_penyewa)
            print("customer age >>>>>>>>>>>>>>", self.umur_penyewa)
            print("customer city >>>>>>>>>>>>>>", self.kota_penyewa)
            print("cost per day >>>>>>>>>>>>>", self.cost_per_day)

    def submit_action(self):
        self.book_status = "submitted"

    def action_cancel(self):
        self.book_status = 'cancel'

    def action_draft(self):
        self.book_status = 'draft'

    @api.onchange('ride_start_dt', 'ride_end_date')
    def _date_difference(self):
        if self.ride_start_dt and self.ride_end_date:
            if self.ride_start_dt > self.ride_end_date:
                raise ValidationError('Donchangeate_in tidak boleh lebih dari Date_out.')
            # self.days_interval = 0
            if self.ride_start_dt < self.ride_end_date:
                day_calc = (self.ride_end_date - self.ride_start_dt).days
                self.days_interval = day_calc

    @api.onchange('days_interval', 'cost_per_day', 'driver_req')
    def _calculate_total(self):
        if self.days_interval == 0:
            if self.driver_req:
                self.total_cost = self.cost_per_day + 1500
            else:
                self.total_cost = self.cost_per_day
        else:
            if self.driver_req:
                self.total_cost = self.days_interval * (self.cost_per_day + 1500)
            else:
                self.total_cost = self.days_interval * self.cost_per_day

    @api.constrains('car1')
    def check_availability(self):
        same_car = self.env['efulrental.booking'].sudo().search([('id', '!=', self.id)])
        print("whole record >>>>>>>>>>>>>>>", same_car)
        for rec in same_car:
            print("rec.car1rec.car1rec.car1", rec.car1)
            if rec.car1 == self.car1:
                date1_start = rec.ride_start_dt
                print('date1 start >>>>>>>>>>>', date1_start)
                date1_end = rec.ride_end_date
                print('date1 end >>>>>>>>>>>', date1_end)
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
                    raise ValidationError("Mobil yang dipilih tidak tersedia! Silahkan Pilih yang lain.")
    
    def create_booking(self):
        name = self.env['efulrental.booking'].create({})
        name.write({
            'nama_penyewa': self.nama_penyewa,
            'email_penyewa': self.email_penyewa,
            'notelp_penyewa': self.notelp_penyewa,
            'umur_penyewa': self.umur_penyewa,
            'kota_penyewa': self.kota_penyewa,
            'driver_req': self.driver_req,
            'ride_start_dt': self.ride_start_dt,
            'ride_end_date': self.ride_end_date,
            'checkout_time_slots': self.checkout_time_slots,
            'car1': self.car1,
            'days_interval': self.days_interval,
            'cost_per_day': self.cost_per_day,
            'total_cost': self.total_cost,
            'book_status': self.book_status,
            'ride_booked': self.ride_booked,
        })