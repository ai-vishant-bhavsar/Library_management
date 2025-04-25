from odoo import http
from odoo.http import request


class CustomerController(http.Controller):

    @http.route('/customer/details', type='json', auth='public', methods=['POST'])
    def get_customer_details(self, email):
        if not email:
            return {'error': 'Email is required'}

        customer = request.env['res.partner'].sudo().search([('email', '=', email)], limit=1)

        if not customer:
            return {'error': 'Customer not found'}

        return {
            'name': customer.name,
            'email': customer.email,
            'phone': customer.phone,
            'company': customer.company_id.name if customer.company_id else '',
        }


class CustomerWebPage(http.Controller):

    @http.route('/customer/fetch', type='http', auth='public', website=True)
    def customer_fetch_page(self, **kwargs):
        return request.render('ak_library_management.customer_page')
