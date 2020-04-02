# -*- coding: utf-8 -*-

from odoo import fields, models

class FshareLink(models.Model):
    _name = "fshare.link"

    name = fields.Char()
