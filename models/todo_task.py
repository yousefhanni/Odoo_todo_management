from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ToDoTask(models.Model):
    _name = 'todo.task'
    _description = 'Task'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Task Name', required=True)
    # Add the ref field for the sequence
    ref = fields.Char(readonly=True, default='New')
    assigned_to = fields.Many2one('res.users', string='Assigned To')
    description = fields.Text(string='Description', tracking=True)
    deadline = fields.Date(string='Deadline')
    is_late=fields.Boolean()

    status = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('complete', 'Complete'),
        ('closed', 'Closed'),
    ], string='Status', default='new', tracking=True)
   
    line_ids = fields.One2many('task.line', 'task_id', string="Task Lines")
    estimated_time = fields.Float(string='Estimated Time')
    total_time = fields.Float(string='Total Time',compute='_compute_total_time')
    
    active=fields.Boolean(default=True)
    
    # Sequence logic
    @api.model_create_multi
    def create(self, vals_list):
        res = super(ToDoTask, self).create(vals_list)
        if res.ref == "New":
            res.ref = self.env["ir.sequence"].next_by_code("todo.task_seq")
        return res
    
    @api.depends('line_ids.time_spent')
    def _compute_total_time(self):
        for task in self:
            task.total_time=sum(task.line_ids.mapped('time_spent'))
            
            
    @api.constrains('total_time', 'estimated_time')
    def _check_time_exceeds(self):
            """ Ensure total time does not exceed estimated time """
            for task in self:
                if task.total_time > task.estimated_time:
                    raise ValidationError("Total time spent ({}) exceeds the estimated time ({})!".format(task.total_time, task.estimated_time))
        
    
    def change_status(self):
        for task in self:
            if task.status == 'new':
                task.status = 'in_progress'
            elif task.status == 'in_progress':
                task.status = 'complete'
            elif task.status == 'complete':
                task.status = 'new'
                
    # Server action
    def action_closed(self):
        for rec in self:
            rec.status = 'closed'
    
    # Automated action
    def check_deadline(self):
        print(self)
        todo_ids = self.search([])  # return all records       
        for rec in todo_ids:
            if rec.status in ['new', 'in_progress']:
                if rec.deadline and rec.deadline < fields.Date.today():
                    rec.is_late = True 
                    
class TaskLine(models.Model):
    _name = "task.line"
    _description = "Task Line"

    description = fields.Text(string="Description")
    time_spent = fields.Float(string="Time Spent")
    finished_time = fields.Datetime(string="Finished Time")
    task_id = fields.Many2one("todo.task", string="Task", ondelete='cascade')

