from odoo import http
from odoo.http import request, route


class ContactController(http.Controller):
    """ This is to make a controller to see the view of contacts on the website """

    @http.route('/contacts', type='http', auth='public', website=True)
    def contact_list(self, **kwargs):
        """ This method patches the all contacts from res.partner model """
        contacts = request.env['res.partner'].sudo().search([])
        return http.request.render('ak_library_management.contact_kanban_page', {'contacts': contacts})

    @http.route(['/contacts/<model("res.partner"):contact_id>'], type='http', auth='public', website=True)
    def contact_detail(self, contact_id):
        """ This method is patch one contact details form
        res.partner model which we click on the front end side"""
        contact = request.env['res.partner'].sudo().browse(contact_id.id)
        if not contact.exists():
            return http.request.not_found()
        return http.request.render('ak_library_management.contact_detail_page', {'contact': contact})
