{
    'name': 'To Do Task',
    'author': 'jo',
    'version': '17.0.0.1.0',
    'description': 'This is a module for managing To Do Task',
    'depends': ['base', 'mail'],
    'data': [
        # 'security/task_assignment_model.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/base_menu.xml',
        'wizard/Task_assignment_wizard_view.xml',
        'views/todo_task_view.xml',
        'reports/todo_report.xml',
        'reports/todo_template.xml',
    ],
    'application': True,
    'license': 'LGPL-3',
}