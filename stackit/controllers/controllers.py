# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class StackItController(http.Controller):

    @http.route('/stackit', type='http', auth='public', website=True)
    def stackit_form(self):
        """
           Render the 'Ask a Question' form page.

           This controller serves the /stackit route which displays a form for users to submit new questions.
           Although the route is publicly accessible, you can apply additional logic inside the method
           to restrict it to logged-in users only.
        """
        return request.render('stackit.stackit_form_template')

    @http.route('/stackit/submit', type='http', auth='public', website=True, csrf=False, methods=['POST'])
    def stackit_submit(self, **post):
        """
            Handle submission of a new question from the StackIt form.

            This controller processes the POST request from the question submission form.
            It extracts the title, description, and comma-separated tags from the form data,
            creates any missing tags, and saves the question to the `stackit.question` model.

            Public users can access this route, but you can add a check to restrict submissions
            to authenticated users if required.

            :param post: Dictionary containing form data ('title', 'description', 'tags').
            :type post: dict
            :return: Redirect response to the form page after successful submission.
            :rtype: werkzeug.wrappers.Response
        """
        title = post.get('title')
        description = post.get('description')
        tags = post.get('tags')

        tag_names = [tag.strip() for tag in tags.split(',') if tag]
        tag_ids = []

        Tag = request.env['stackit.tag'].sudo()
        for tag_name in tag_names:
            tag = Tag.search([('name', '=', tag_name)], limit=1)
            if not tag:
                tag = Tag.create({'name': tag_name})
            tag_ids.append(tag.id)
        # Save to custom model (optional)
        request.env['stackit.question'].sudo().create({
            'title': title,
            'description': description,
            'tag_ids': [(6, 0, tag_ids)],
        })

        request.env['bus.bus']._sendone(
            request.env.user.partner_id,
            'simple_notification',
            {
                'type': 'success',
                'message': "Question is submitted",
            }
        )

        return request.redirect('/stackit')

    @http.route('/questions', type='http', auth='public', website=True)
    def all_questions(self):
        """
            Render the page displaying all submitted questions.

            This controller fetches all records from the `stackit.question` model 
            and renders them using the `questions_list_template`. It is accessible 
            publicly via the website.

            :return: Rendered template displaying the list of all questions.
            :rtype: werkzeug.wrappers.Response
        """
        questions = request.env['stackit.question'].sudo().search([])
        return request.render('stackit.questions_list_template', {
            'questions': questions
        })

    @http.route('/questions/<int:question_id>', type='http', auth='public', website=True)
    def question_answer_detail(self, question_id, **kw):
        """
           Render the detail page for a specific question, including its answers.

           This controller handles the display of a single question based on its ID.
           It fetches the question from the `stackit.question` model and renders it
           using the `question_detail_template`. All related answers are shown in
           the template.

           :param int question_id: The ID of the question to display.
           :param dict kw: Additional keyword arguments (unused).
           :return: Rendered HTML page for the specific question and its answers.
           :rtype: werkzeug.wrappers.Response
        """
        question = request.env['stackit.question'].sudo().browse(question_id)
        return request.render('stackit.question_detail_template', {
            'question': question
        })

    @http.route('/questions/give_answer/<int:question_id>', type='http', auth='user', website=True, csrf=False,
                methods=['POST'])
    def give_answer_post(self, question_id, **post):
        """
            Handle submission of a new answer to a specific question.

            This controller method is called via POST when a user submits an answer
            to a question from the website. It creates a new record in the
            `stackit.answer` model linked to the given question and the logged-in user.

            Additionally, it sends a simple browser bus notification to confirm
            success using the `bus.bus` service.

            Route: /questions/give_answer/<question_id>
            Auth: User (must be logged in)
            CSRF: Disabled for simplicity (can be enabled if desired)

            :param int question_id: ID of the question being answered.
            :param dict post: Dictionary containing the submitted form data.
                              Expected key: 'answer'
            :return: Redirects the user back to the list of questions.
            :rtype: werkzeug.wrappers.Response
        """
        answer_text = post.get('answer')
        if answer_text:
            request.env['stackit.answer'].sudo().create({
                'question_id': question_id,
                'answer': answer_text,
                'user_id': request.env.uid,
            })

            request.env['bus.bus']._sendone(
                request.env.user.partner_id,
                'simple_notification',
                {
                    'type': 'success',
                    'message': "Answer is submitted",
                }
            )

        return request.redirect('/questions')