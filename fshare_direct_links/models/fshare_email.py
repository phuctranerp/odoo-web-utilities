# -*- coding: utf-8 -*-

from odoo import fields, models

class FshareEmail(models.Model):
    _name = "fshare.email"

    name = fields.Char()
