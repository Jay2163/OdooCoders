# -*- coding: utf-8 -*-

from odoo import models, fields


class StackItTag(models.Model):
    _name = 'stackit.tag'
    _description = 'Q&A Tag'

    name = fields.Char(required=True)