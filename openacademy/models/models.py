import re
import random
from odoo.exceptions import  ValidationError
from odoo import fields, models, api, _
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

class Course(models.Model):
    _name = 'openacademy.course'
    _description = "OpenAcademy Courses"
    _rec_name='course_category'

    course_category = fields.Char(string="Title", required=True)
    description = fields.Text()

class Coursetype(models.Model):
    _name = 'openacademy.coursetype'
    _description = "OpenAcademy Course Category"
#    __stream='course stream'
#    __rate='courserate'
    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    rate = fields.Float()
    #category=fields.Selection([('ms','Medical Science'),('arts','Arts'),('eng','Engineering'),('psy','Psychology'),('mng_mnt','Management')],required="True",string="Course Category")
    courses_catagory=fields.Many2one('openacademy.course')
    course_pay_type=fields.Selection([('free','Free'),('paid','Paid')], default="paid",String="Course Cost")
    hide = fields.Boolean(string='Hide', compute="_compute_hide")

    @api.depends('course_pay_type')
    def _compute_hide(self):
        # simple logic, but you can do much more here
        if self.course_pay_type == 'free':
            self.rate="00.00"
            self.hide = True
        else:
            self.hide = False

class Workshop(models.Model):
     _name = 'openacademy.workshop'
     _description = "OpenAcademy Workshops"

     name = fields.Text()
     date = fields.Date()
     time = fields.Float()
     fee  = fields.Float()
     place = fields.Text()
     instructor =fields.Many2one('openacademy.instructor.information',string=" Instructor",required="True")
     exam = fields.Text(string="Exam Duration")
     modules_Number=fields.Integer(string="Number of Modules")


class Instructor(models.Model):
     _name='openacademy.salary'
     _description = "OpenAcademy Instructor Salary"
     _rec_name='instructor_name'


     #instructor_name=fields.Char(string="Name",required="True")
     instructor_name=fields.Many2one('openacademy.instructor.information',string="Name",required="True")
     pay_per_hour=fields.Float(string="Pay per hour")
     working_hour=fields.Integer("Working Hour")
     salary= fields.Float( compute='_compute_totalsalary')

     @api.depends('working_hour','pay_per_hour')
     def _compute_totalsalary(self):
         for record in self:
             record.salary = record.pay_per_hour * record.working_hour

     # @api.onchange('working_hour','pay_per_hour')
     # def _onchange_salary(self):
     #     self.salary = self.pay_per_hour* self.working_hour


class InstructorInfo(models.Model):
     _name='openacademy.instructor.information'
     _description = "OpenAcademy Instructor Info"
     _rec_name='instruct_name'

     instruct_name=fields.Char(string="Name")
     contact=fields.Char(string="Contact")
     address=fields.Text(string="Address")
     country_id = fields.Many2one('res.country', string='Country', help='Select Country', ondelete='restrict')
     state_id = fields.Many2one('res.country.state', string='State', help='Enter State', ondelete='restrict')
     city = fields.Char(string="City", help='Enter City')
     hide = fields.Boolean(string='Hide', compute="_compute_hide")

     email=fields.Char(string="Email")

     @api.onchange('country_id')
     def _onchange_country_id(self):
         if self.country_id:
             return {'domain': {'state_id': [('country_id', '=', self.country_id.id)]}}
         else:
             return {'domain': {'state_id': []}}

# Show Hide State selection based on Country
     @api.depends('country_id')
     def _compute_hide(self):
         if self.country_id:
             self.hide = False
         else:
             self.hide = True

     @api.constrains('contact')
     def _contact_constrains(self):
            for re in self:
                val=re.contact
                if val.isdigit() and len(val)==10:
                    return True
                else:
                    return False
     _constraints = [(_contact_constrains,'Enter 10 Digits Number', ['contact']),]


     @api.constrains('email')
     def _validate_email(self):
             self.email.replace(" ","")
             if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
                 raise ValidationError("Please Enter Valid Email Address!!")

     _sql_constraints = [
                 ('email_unique',
                 'UNIQUE(email)',
                 "The Email must be unique"),
      ]




class Enrolled(models.Model):
     _name='openacademy.enrolledstudent'
     _description = "OpenAcademy Enrolled Students"
     _rec_name='stu_name'


     stu_photo=fields.Binary('Profile Picture')
     stu_name=fields.Char(string="Student Name",required='True')
     contact=fields.Char(string="Contact Number")
     email=fields.Char(string="Email", required='True')
     qualification= fields.Selection([('graduate','Graduate'),('ug','Under Graduate'),('pg','Post Graduate')], default="graduate", string="Qualification")
     gender=fields.Selection([('male','Male'),('female','Female')], default="male",String="Gender")
     birthday=fields.Date("D-O-B")
     age=fields.Integer("Age")
     no_course = fields.Integer()
     course_unit_cost = fields.Float(default="1200.00")
     total_course_fees =fields.Float( string="Total Fees", compute='_compute_totalfees')
     sub1=fields.Float(string="Science")
     sub2=fields.Float(string="Maths")
     sub3=fields.Float(string="Physics")
     percentage=fields.Float(string="percentage")
     status=fields.Char(string="Status", compute='_compute_result_status')


     @api.depends('no_course','course_unit_cost')
     def _compute_totalfees(self):
         for record in self:
             self.total_course_fees = self.no_course * self.course_unit_cost
     @api.depends('percentage')
     def _compute_result_status(self):
         for record in self:
             if record.percentage >= 45:
                 record.status = "PASS"
             else:
                 record.status = "Fail"

     @api.onchange('sub1','sub2','sub3')
     def _find_percentage(self):
         self.percentage= (self.sub1 + self.sub2 +self.sub3 )/3

     @api.constrains('sub1')
     def _check_number(self):
            sub1 = self.sub1
            if sub1 and len(str(abs(sub1))) >= 100:
	            raise ValidationError(_('Number of digits must not on exceed 100'))

    #  @api.onchange('no_course', 'course_unit_cost')
    #  def _onchange_price(self):
    # # set auto-changing field
    #     self.total_course_fees = self.no_course * self.course_unit_cost

     @api.onchange('birthday')
     def  _onchange_age(self):
            if self.birthday:
                years= relativedelta(date.today(), self.birthday).years
                self.age=years

     @api.constrains('contact')
     def _contact_constrains(self):
            for re in self:
                val=re.contact
                if val.isdigit() and len(val)==10:
                    return True
                else:
                    return False
     _constraints = [(_contact_constrains,'Enter 10 Digits Number', ['contact']),]


     @api.constrains('email')
     def _validate_email(self):
            self.email.replace(" ","")
            if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
                raise ValidationError("Please Enter Valid Email Address!!")

     _sql_constraints = [
                ('email_unique',
                'UNIQUE(email)',
                "The Email must be unique"),
     ]



class CourseEnrolled(models.Model):
    _name='openacademy.courseenrolled'
    _description='Courses Enrollment'
    _rec_name='course_name'

    course_name=fields.Many2one('openacademy.coursetype')
    enrolledstudent=fields.Many2many('openacademy.enrolledstudent',string="Student Name")

class RegisteredStudents(models.Model):
    _name='openacademy.registered.student'
    _description='Registered Students'
    _rec_name='regi_no'

    regi_no = fields.Char(string='Registration Number', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    student_name=fields.Many2one('openacademy.enrolledstudent', string="Name")
    contact=fields.Char(string="Contact Number", related="student_name.contact")
    email_id=fields.Char(string="Email", related="student_name.email")
    hobbies=fields.Char(string="Hobbies" ,readonly=True)

    pay_on=fields.Boolean('Online')
    pay_off=fields.Boolean('Offline')
    pay_oth=fields.Boolean('Other')

    payment_status=fields.Selection([('done','Done'),('pending','Pending')], default="pending",String="Payment Status")

    regi_date=fields.Datetime()
    enrolledcourses_line=fields.One2many('openacademy.registeredcourse.line','coursetype',string ="Add course line")
    state=fields.Selection([('done','Done'),('cancel','Cancelled')],required=True, default='cancel')
    confirmation_date=fields.Datetime()
    regi_date=fields.Datetime(string="Registration Date",required=True, readonly=True, index=True,copy=False, default=fields.Datetime.now)

    amount_totalcost = fields.Float(string='Course Amount',compute='_amount_all',store=True, readonly=True, track_visibility='onchange')
    amount_discounted = fields.Float(string='Discount', compute='_amount_all', store=True, readonly=True)
    amount_total = fields.Float(string='Total',compute='_amount_all', store=True, readonly=True)

    # @api.depends('pay_on','pay_off','pay_oth')
    # def _hobbies_checked(self):
    #     hobbie=""
    #     for record in self:
    #         if self.pay_on is True:
    #             hobbie+="Online ,"
    #             print(hobbie)
    #         elif self.pay_off is True:
    #             hobbie+="Offline ,"
    #         elif self.pay_oth is True:
    #             hobbie+="Other"
    #         else :
    #             print("nothing selected")
    #     print(hobbie)



    @api.depends('enrolledcourses_line.rate','enrolledcourses_line.discount')
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
             amount_totalcost = amount_discounted =  0.0
             for line in order.enrolledcourses_line:
                amount_totalcost += line.rate
                amount_discounted += (line.rate * line.discount)/100

             order.update({
                'amount_totalcost': amount_totalcost,
                'amount_discounted': amount_discounted,
                'amount_total': amount_totalcost - amount_discounted,
            })



    @api.model
    def create(self, vals):
        if vals.get('regi_no', _('New')) == _('New'):
            vals['regi_no'] = self.env['ir.sequence'].next_by_code(
                'self.service') or _('New')
        result = super(RegisteredStudents, self).create(vals)
        return result
        
    @api.multi
    def action_confirm(self):
        for rec in self:
            rec.write({'state':'done','confirmation_date': fields.Datetime.now()})

    @api.multi
    def action_cancel(self):
        for rec in self:
            rec.write({'state': 'cancel'})

    @api.multi
    def action_prints(self):
        # mail = self.env['openacademy.registered.student'].browse(self.email_id.id)
        print("Button clicked")
        return self.env.ref('openacademy.action_report_course_receipt').report_action(self)

    # # def fetch_email(self):
    #     mail = self.env['openacademy.registered.student'].browse(self.email_id.id)
    #     print("email id", mail)
    #     # print("sendig mail")
    #     # template_id=self.env.ref('openacademy.sendemail_template').id
    #     # print("template id",template_id)
    #     # template=self.env['mail.template'].browse(template_id)
    #     # print("template",template)
    #     # template.send_mail(self.id,force_send=True)

    def action_send_mail(self):
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference('openacademy', 'sendemail_template')[1]
        except ValueError:
            template_id = False
        try:
                compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = {
        'default_model': 'openacademy.registered.student',
        'default_res_id': self.ids[0],
        'default_use_template': bool(template_id),
        'default_template_id': template_id,
        'default_composition_mode': 'comment',
        'mark_so_as_sent': True,
        'force_email': True
        }
        return {
        'type': 'ir.actions.act_window',
        'view_type': 'form',
        'view_mode': 'form',
        'res_model': 'mail.compose.message',
        'views': [(compose_form_id, 'form')],
        'view_id': compose_form_id,
        'target': 'new',
        'context': ctx,
        }




class RegisteredCourseLines(models.Model):
    _name='openacademy.registeredcourse.line'
    _description = "OpenAcademy Registered Course Line"

    coursetype=fields.Many2one('openacademy.registered.student',string="Course Name")
    name=fields.Many2one('openacademy.coursetype',string="Course Type")
    rate=fields.Float(string="Rate")
    courses_catagory=fields.Many2one('openacademy.course')
    discount=fields.Float(string="Discount %")




    @api.onchange('name')
    def _onchange_name(self):
        print("on change method calling ", self.name)
        if self.name:
            self.rate=self.name.rate
            self.courses_catagory=self.name.courses_catagory

class Opencalender(models.Model):
    _name='openacademy.calender'
    _description = "Entry in Calender"
    _rec_name='emp_name'
    emp_name=fields.Char(string="Name")
    entrycalender_line=fields.One2many('openacademy.entrycalender','link' ,string ="Add course line", default=[
         (0,0,{'week_day': 'mon', 'start_time': 10.00, 'end_time': 19.00}),
         (0,0,{'week_day': 'tue','start_time': 10.00, 'end_time': 19.00}),
         (0,0,{'week_day': 'wed','start_time': 10.00, 'end_time': 19.00}),
         (0,0,{'week_day': 'thu','start_time': 10.00, 'end_time': 19.00}),
         (0,0,{'week_day': 'fri','start_time': 10.00, 'end_time': 19.00}),
         (0,0,{'week_day': 'sat','start_time': 10.00, 'end_time': 19.00}),
         (0,0,{'week_day': 'sun','start_time': 10.00, 'end_time': 19.00})
        ])

class Entrycalender(models.Model):
    _name='openacademy.entrycalender'
    _description="Timing Calculation"

    link=fields.Many2one('openacademy.calender',string="link Name")
    week_day= fields.Selection([('mon','Monday'),('tue','Tuesday'),('wed','Wednesday'),('thu','Thursday'),('fri','Friday'),('sat','Saturday'),('sun','Sunday')],required=True, string="Week Day")
    start_time= fields.Float('Starting Time')
    end_time = fields.Float('Ending Time')

class Paymentstatus(models.TransientModel):
    _name='openacademy.wizardpayment'
    _description="Wizard Payment"

    payment_status=fields.Selection([('done','Done'),('pending','Pending')], default="pending",String="Payment Status")

    @api.multi
    def set_pay_status(self):
        records=self.env['openacademy.registered.student'].browse(self.env.context.get('active_ids'))
        records.write({'payment_status':self.payment_status})
