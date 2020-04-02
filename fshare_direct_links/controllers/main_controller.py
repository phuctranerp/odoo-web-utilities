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
        print ("OKKKKK")
        # Get link
        connector = request.env['fshare.connector'].sudo().search([], limit=1)
        print(connector)
        if not connector:
            return "Unable to get link"
        
        return connector.get_fshare_link(url)
