# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class Academy(http.Controller):
    @http.route('/fshare', auth='public', website=True)
    def index(self, **kw):
        return request.render('fshare_direct_links.fshare_get_link_form')

    @http.route('/get_fshare_direct_link', auth='public')
    def get_fsharelink(self, **kw):
        url = kw.get("url")
        # Get link
        connector = request.env['fshare.connector'].sudo().search([], limit=1)
        print(connector)
        if not connector:
            return "Unable to get link"
        
        return connector.get_fshare_link(url)

    @http.route('/giveaway', auth='public', website=True)
    def index_giveaway(self, **kw):
        return request.render('fshare_direct_links.fshare_giveaway')


    @http.route('/submit_giveaway_email', auth='public')
    def submit_giveaway_email(self, **kw):
        email = kw.get("email")

        # Checking for slots available
        max_count = int(request.env["ir.config_parameter"].sudo().get_param(
            "no_fshare_giveaway", default='0'))
        
        # Check for existing
        emails = request.env["fshare.email"].sudo().search([]).mapped("name")
        no_emails = len(set(emails))
        if no_emails >= max_count:
            return "rejected"
        
        request.env["fshare.email"].sudo().create({'name': email})
        return "accepted"
