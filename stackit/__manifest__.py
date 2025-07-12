# -*- coding: utf-8 -*-
{
    'name': 'Stackit',
    'version': '18.0.1.0.0',
    'author': 'Jay Butani',
    'sequence': 5,
    'summary': 'Stackit Module',
    'description': "StackIt is a minimal, user-friendly Q&A platform that enables collaborative "
                   "learning and structured knowledge sharing through features "
                   "like rich text editing, tagging, voting, and real-time "
                   "notifications.",
    'data': [
        "security/ir.model.access.csv",
        "views/stackit_question_views.xml",
        # "views/stackit_answer_views.xml",
        "views/stackit_tag_views.xml",
        'views/stackit_views.xml',
        # 'views/templates.xml',
    ],
    'assets': {
        'web.assets_frontend' : [
            'stackit/static/src/js/answer.js',
        ]
    },
    'depends':['base','website'],
    'application': True,
    'license': 'LGPL-3',
}

