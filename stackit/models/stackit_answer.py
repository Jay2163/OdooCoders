# -*- coding: utf-8 -*-

from odoo import models, fields


class StackItAnswer(models.Model):
    _name = 'stackit.answer'
    _description = 'Q&A Answer'

    question_id = fields.Many2one('stackit.question', required=True, string="Question")
    answer = fields.Html(required=True, string="Answer")
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user.id, string="user")