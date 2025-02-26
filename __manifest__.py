{
    'name': 'To Do Task',
    'author': 'jo',
    'version': '17.0.0.1.0',
    'description': 'This is a module for managing To Do Task',
    'depends': ['base','mail'],
    'data': [
    'security/ir.model.access.csv',
    'views/base_menu.xml',
    'views/todo_task_view.xml',
    'reports/todo_report.xml',   # Ensure this is included
    'reports/todo_template.xml', # Ensure this is included
],

    'application': True,
}
