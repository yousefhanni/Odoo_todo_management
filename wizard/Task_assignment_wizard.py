from odoo import models, fields, api
from odoo.exceptions import ValidationError

class BulkTaskAssignmentWizard(models.TransientModel):
    _name = 'bulk.task.assignment.wizard'
    _description = 'Bulk Task Assignment Wizard'

    assigned_to = fields.Many2one('res.users', string='Assign To', required=True)

    def action_assign_tasks(self):
        task_ids = self.env.context.get('active_ids', [])
        if not task_ids:
            raise ValidationError("No tasks selected to assign!")
        tasks = self.env['todo.task'].browse(task_ids)
        if not tasks:
            raise ValidationError("No valid tasks found to assign!")
        invalid_tasks = []
        for task in tasks:
            if task.status not in ['new', 'in_progress']:
                invalid_tasks.append(task.name)
        if invalid_tasks:
            raise ValidationError(
                "You can only assign tasks with status 'New' or 'In Progress'. "
                "The following tasks are invalid: %s" % ', '.join(invalid_tasks)
            )
        tasks.write({'assigned_to': self.assigned_to.id})
        return {'type': 'ir.actions.act_window_close'}
    