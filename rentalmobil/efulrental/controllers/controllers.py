from odoo import http, models, fields
from odoo.http import request
import json

class efulrental(http.Controller):
    @http.route('/efulrental/getstokmobil', auth='public', method=['GET'])
    def getStokmobil(self, **kw):
        stokmobil = request.env['efulrental.stokmobil'].search([])
        isi = []
        for bb in stokmobil:
            isi.append({
                'nama_mobil' : bb.nama_mobil,
                'tipe_mobil' : bb.tipe_mobil,
                'brand' : bb.brand,
                'harga_sewa' : bb.harga_sewa,
                'car_status' : bb.car_status
            })
        return json.dumps(isi)

    @http.route('/efulrental/getpenyewa', auth='public', method=['GET'])
    def getPenyewa(self, **kw):
        penyewa = request.env['efulrental.penyewa'].search([])
        pen = []
        for s in penyewa:
            pen.append({
                'nama_perusahaan' : s.name,
                'alamatlengkap' : s.alamatlengkap,
                'notelp' : s.notelp,
                'email' : s.email,
                'umur' : s.umur,
                'status' : s.status
            })
        return json.dumps(pen)