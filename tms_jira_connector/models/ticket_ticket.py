# -*- coding: utf-8 -*-

from odoo import api, fields, models

class TicketTicket(models.Model):
    _name = "ticket.ticket"

    name = fields.Char(compute="_compute_ticket_name")
    issue_type = fields.Selection([('Story', 'Story')], default="Story")
    connector_id = fields.Many2one(
        "jira.connector", "Connector",
        default=lambda r: r.env["jira.connector"].search([], limit=1))
    tms_ref = fields.Char("TMS Ticket")
    jira_ref = fields.Char("Jira Ticket")
    jira_task_id = fields.Integer("Jira Ticket ID")
    summary = fields.Char("Description")
    description = fields.Text("Content")

    def get_tms_data(self):
        for ticket in self:
            ticket.connector_id.get_tms_ticket_data(ticket)

    def create_jira_task(self):
        for ticket in self:
            ticket.connector_id.create_jira_task(ticket)

    def _compute_ticket_name(self):
        for ticket in self:
            ticket.name = "[%s] %s" % (self.tms_ref or "", self.summary or "")
