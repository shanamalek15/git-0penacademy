from odoo import http
from odoo.http import request
class MyWeb(http.Controller):
    @http.route('/myweb', auth='public', website=True)
    def index(self, **kw):
        # return "Hello, world"
        details=http.request.env['openacademy.registered.student'].sudo().search([])
        return http.request.render('openacademy.my_home_page')

    @http.route('/secondpage', auth='public', website=True)
    def second(self, **kw):
        # return "Hello, world"
        return http.request.render('openacademy.course_second_page', {'my_details': {}})
