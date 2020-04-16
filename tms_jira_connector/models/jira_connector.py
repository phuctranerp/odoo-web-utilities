# -*- coding: utf-8 -*-

from odoo import api, models, fields
import odoorpc
import json
import urllib.request
import requests
from odoo.exceptions import UserError
from requests.auth import HTTPBasicAuth


class JiraConnector(models.Model):
    _name = "jira.connector"

    name = fields.Char()
    jira_url = fields.Char("Jira URL")
    jira_email = fields.Char("Jira Email")
    jira_token = fields.Char("Jira Token")
    jira_project_key = fields.Char()
    tms_path = fields.Char("TMS Path")
    tms_db = fields.Char("TMS DB")
    tms_auth_user = fields.Char("TMS Auth User")
    tms_auth_pass = fields.Char("TMS Auth Pass")
    tms_username = fields.Char("TMS Username")
    tms_password = fields.Char("TMS Password")
    default_assignee = fields.Char()

    def mass_assigning_task(self):
        self.ensure_one()
        tickets = self.env["ticket.ticket"].search(
            [("connector_id", "=", self.id)])
        for ticket in tickets:
            try:
                self.assign_task(ticket)
            except Exception:
                continue

    def get_jira_authen(self):
        BASIC_AUTH = HTTPBasicAuth(self.jira_email, self.jira_token)
        HEADERS = {'Content-Type' : 'application/json;charset=iso-8859-1'}
        return BASIC_AUTH, HEADERS

    def get_all_tms_data(self):
        self.ensure_one()
        tickets = self.env["ticket.ticket"].search(
            [("connector_id", "=", self.id)])
        for ticket in tickets:
            self.get_tms_ticket_data(ticket)

    def get_tms_ticket_data(self, ticket):
        self.ensure_one()
        # Prepare connection
        pwd_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        pwd_mgr.add_password(
            None, self.tms_path,
            self.tms_auth_user, self.tms_auth_pass
        )
        auth_handler = urllib.request.HTTPBasicAuthHandler(pwd_mgr)
        opener = urllib.request.build_opener(auth_handler)
        tms_connector = odoorpc.ODOO(
            self.tms_path.replace("https://", ""),
            protocol='jsonrpc+ssl',
            port=443,
            opener=opener
        )
        tms_connector.login(self.tms_db, self.tms_username, self.tms_password)

        support_ticket = tms_connector.env["tms.support.ticket"].browse(
            int(ticket.tms_ref.replace("S#", "")))

        ticket.summary = support_ticket.summary
        ticket.description = support_ticket.description

    def create_jira_task(self, ticket):
        """
        Function trigger to create jira task
        """
        self.ensure_one()
        request_url = "%s/rest/api/2/issue/" % self.jira_url

        BASIC_AUTH, HEADERS = self.get_jira_authen()

        data = {
            "fields": {
                "project":
                {
                    "key": self.jira_project_key
                },
                "summary": ticket.name,
                "description": ticket.description and ticket.description.replace("#", "") or "",
                "issuetype": {
                    "name": ticket.issue_type
                },
            }
        }
        response = requests.post(
            request_url,
            headers=HEADERS,
            auth=BASIC_AUTH,
            data=json.dumps(data, indent=4)
        )

        if response.status_code == 201:
            result = json.loads(response.text)
            ticket.write({
                "jira_task_id": result["id"],
                "jira_ref": result["key"]
            })
        else:
            raise UserError(response.text)

    def assign_task(self, ticket):
        self.ensure_one()
        request_url = "%s/rest/api/2/issue/%s/assignee" % (
            self.jira_url, ticket.jira_ref)
        BASIC_AUTH, HEADERS = self.get_jira_authen()

        data = {
            "accountId": self.default_assignee
        }

        res = requests.put(
            request_url,
            headers=HEADERS,
            auth=BASIC_AUTH,
            data=json.dumps(data, indent=4)
        )

        if str(res.status_code) == "204":
            ticket.assigned = True
        else:
            raise UserError(res.text)
