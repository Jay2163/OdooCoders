# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StackItQuestion(models.Model):
    _name = 'stackit.question'
    _description = 'Q&A Question'
    _rec_name = 'title'

    title = fields.Char(string="Title", required=True, tracking=True)
    description = fields.Html(string="Description")
    tag_ids = fields.Many2many('stackit.tag', string="Tags")
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user.id, tracking=True)
    answer_ids = fields.One2many('stackit.answer', 'question_id', string="Answers")
    accepted_answer_id = fields.Many2one('stackit.answer', string="Accepted Answer")
