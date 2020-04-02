# -*- coding: utf-8 -*-

from odoo import api, fields, models
from get_fshare import FSAPI

class FshareConnector(models.Model):
    _name = "fshare.connector"

    name = fields.Char("Connector Name")
    username = fields.Char("Username")
    password = fields.Char("Password")

    def get_fshare_link(self, url):
        """
        @Function to get fshare link
        """
        # Track the link
        self.env["fshare.link"].sudo().create({'name': url})
        session = FSAPI(email=self.username, password=self.password)
        session.login()
        try:
            return session.download(url)
        except Exception:
            return "Invalid URL. Support Single File URL Only"
