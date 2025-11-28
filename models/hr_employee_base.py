from email.policy import default

from odoo import fields, models,api

import logging
_logger = logging.getLogger(__name__)

class HrEmployee(models.Model):
    _inherit = "hr.employee"

    firstname = fields.Char(string="First Name")
    lastname = fields.Char(string="Last Name")
    relationship = fields.Char(string="Relationship")
    preferred_name = fields.Char(string="Preferred Name")
    job_description = fields.Text(string="Job Description")
    rehire_eligibility = fields.Boolean(string="Rehire Eligibility")
    position_code = fields.Char(string="Position Code")
    driver_license_no = fields.Char("Driver License No")
    driver_license_expiry = fields.Date("Driver License Expiry")
    manager_history_ids = fields.One2many('hr.manager.history', 'employee_id', string='Manager History')
    current_contract_reference = fields.Char(string='Current Contract/Period Reference')

    driver_license_attachment = fields.Binary("License Document")

    immigration_documents = fields.One2many(
        "immigration.document",
        "employee_id",
    )

    employment_status = fields.Selection([
        ('active', 'Active'),
        ('terminated', 'Terminated'),
        ('on_leave', 'On Leave'),
        ('on_fmla', 'On FMLA'),
        ('intermittent_fmla', 'On Intermittent FMLA'),
        ('suspended', 'Suspended'),
        ('on_loa', 'On LOA'),
        ('maternity_leave', 'Maternity Leave'),
    ], string="Employment Status", default='active')

    department_history_ids = fields.One2many(
        "hr.employee.department.history",
        "employee_id",
        string="Department History",
    )

    joining_date = fields.Date(string="Joining Date")
    visa_type = fields.Selection([
        ('h1b', 'H-1B'),
        ('h1b_transfer', 'H-1B Transfer'),
        ('h1b_amendment', 'H-1B Amendment'),
        ('h1b_extension', 'H-1B Extension'),
        ('h4', 'H-4'),
        ('l1', 'L-1A/L-1B'),
        ('opt', 'OPT'),
        ('stem_opt', 'STEM OPT'),
        ('tn', 'TN'),
        ('b1_b2', 'B-1/B-2'),
        ('green_card', 'Green Card Processing'),
        ('citizen', 'Citizen'),
        ('other', 'Other'),
    ], string="Visa Type")

    petition_type = fields.Selection([
        ('initial', 'Initial'),
        ('transfer', 'Transfer'),
        ('amendment', 'Amendment'),
        ('extension', 'Extension'),
    ], string="Petition Type")
    petition_number = fields.Char(string="Petition Number")
    uscis_receipt_number = fields.Char(string="USCIS Receipt Number")
    petition_filing_date = fields.Date(string="Petition Filing Date")
    case_status = fields.Selection([
        ('filed', 'Filed'),
        ('rfe', 'RFE'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
        ('withdrawn', 'Withdrawn'),
    ], string="Case Status")
    premium_processing = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], string="Premium Processing")

    rfe_received = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], string="RFE Received")

    rfe_response_date = fields.Date(string="RFE Response Date")


    validity_start_date = fields.Date(string="Validity Start Date")
    validity_end_date = fields.Date(string="Validity End Date")
    i94_expiry_date = fields.Date(string="I-94 Expiry Date")
    passport_expiry_date = fields.Date(string="Passport Expiry Date")
    visa_stamp_expiry_date = fields.Date(string="Visa Stamp Expiry Date")


    lca_number = fields.Char(string="LCA Number")
    lca_filing_date = fields.Date(string="LCA Filing Date")
    lca_posting_start_date = fields.Date(string="LCA Posting Start Date")
    lca_posting_end_date = fields.Date(string="LCA Posting End Date")
    worksites = fields.Selection([
        ('office', 'Office'),
        ('warehouse', 'Warehouse'),
        ('remote', 'Remote Location'),
    ], string="Worksite(s)", multiple=True)
    soc_code = fields.Char(string="SOC Code")
    wage_level = fields.Selection([
        ('level_1', 'Level 1'),
        ('level_2', 'Level 2'),
        ('level_3', 'Level 3'),
        ('level_4', 'Level 4'),
    ], string="Wage Level")
    prevailing_wage = fields.Float(string="Prevailing Wage")
    actual_wage = fields.Float(string="Actual Wage")


    worksite_address = fields.Char(string="Worksite Address")
    lca_job_title = fields.Char(string="LCA Job Title")
    job_location = fields.Selection([
        ('location_1', 'Location 1'),
        ('location_2', 'Location 2'),
        ('location_3', 'Location 3'),
    ], string="Job Location")
    standard_work_hours = fields.Float(string="Standard Work Hours")
    job_duties_changed = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], string="Change in Job Duties Since Last Filing")

    new_lca_needed = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], string="New LCA Needed?")

    forklift_license_number = fields.Char(string="Forklift License Number")


    law_firm_name = fields.Char(string="Law Firm Name")
    attorney_assigned = fields.Char(string="Attorney Assigned")
    attorney_email = fields.Char(string="Attorney Email")
    attorney_phone = fields.Char(string="Attorney Phone Number")
    attorney_note = fields.Text(string="Attorney Note")


    employee_type = fields.Selection([
        ('us_employee', 'US Employee (W2)'),
        ('independent_contractor_us', 'Independent Contractor – US (1099)'),
        ('overseas_contractor', 'Overseas Independent Contractor'),
        ('staffing_employee', 'Staffing Employee'),
        ('intern', 'Intern'),
        ('temp_to_hire', 'Temp-to-Hire'),
    ], string="Employee Type")

    # Map employee type to group XML ID
    EMPLOYEE_TYPE_TO_GROUP = {
        'us_employee': 'employee_information.group_us_employee',
        'independent_contractor_us': 'employee_information.group_independent_contractor_us',
        'overseas_contractor': 'employee_information.group_overseas_contractor',
        'staffing_employee': 'employee_information.group_staffing_employee',
        'intern': 'employee_information.group_intern',
        'temp_to_hire': 'employee_information.group_temp_to_hire',
    }

    ssnid = fields.Char(
        string='SSN',
        groups="base.group_system,employee_information.group_hr_managers"
    )

    ssnid_masked = fields.Char(
        string='SSN',
        compute='_compute_ssnid_masked',
        store=False
    )


    @api.depends('ssnid')
    def _compute_ssnid_masked(self):
        for record in self:
            if record.ssnid:
                # Show format: ***-**-1234 (last 4 digits)
                if len(record.ssnid) >= 4:
                    record.ssnid_masked = '***-**-' + record.ssnid[-4:]
                else:
                    record.ssnid_masked = '****'
            else:
                record.ssnid_masked = ''

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        """Override to show appropriate field based on permissions"""
        res = super().fields_get(allfields, attributes)
        if 'ssnid' in res and not (
                self.env.user.has_group('base.group_system') or
                self.env.user.has_group('employee_information.group_hr_managers')
        ):
            res['ssnid']['invisible'] = True
        return res

    @api.model
    def create(self, vals):
        employee = super(HrEmployee, self).create(vals)
        if employee.employee_type and employee.user_id:
            group_xml_id = self.EMPLOYEE_TYPE_TO_GROUP.get(employee.employee_type)
            if group_xml_id:
                group = self.env.ref(group_xml_id)
                group.users |= employee.user_id
        return employee

    def write(self, vals):
        if 'employee_type' in vals:
            self._remove_from_all_employee_type_groups()

        if 'parent_id' in vals:
            for record in self:
                old_manager = record.parent_id.id if record.parent_id else False
                new_manager = vals.get('parent_id')
                if old_manager != new_manager:
                    self.env['hr.manager.history'].create_manager_history(
                        employee_id=record.id,
                        old_manager_id=old_manager,
                        new_manager_id=new_manager,
                        contract_ref=record.current_contract_reference
                    )

        if 'department_id' in vals:
            for employee in self:
                self.env['hr.employee.department.history'].create({
                    'employee_id': employee.id,
                    'department_id': vals['department_id'],
                    'start_date': fields.Date.today(),
                })

        result = super().write(vals)

        if 'employee_type' in vals:
            self._update_employee_type_group()

        return result

    def _remove_from_all_employee_type_groups(self):
        """Remove the user from every employee-type group."""
        all_groups = self.env['res.groups']
        for xml_id in self.EMPLOYEE_TYPE_TO_GROUP.values():
            group = self.env.ref(xml_id, raise_if_not_found=False)
            if group:
                all_groups |= group

        for employee in self.filtered('user_id'):
            all_groups.write({'user_ids': [(3, employee.user_id.id)]})

    def _update_employee_type_group(self):
        """Add the user to the group that matches the new employee_type."""
        for employee in self.filtered('user_id'):
            new_type = employee.employee_type
            xml_id = self.EMPLOYEE_TYPE_TO_GROUP.get(new_type)
            if not xml_id:
                _logger.warning('No group mapping for employee_type %r', new_type)
                continue
            group = self.env.ref(xml_id, raise_if_not_found=False)
            if group:
                group.write({'user_ids': [(4, employee.user_id.id)]})
            else:
                _logger.error('Group XML-ID %s not found', xml_id)


    def action_manager_history(self):
        """Open manager history view"""
        self.ensure_one()
        return {
            'name': 'Manager History',
            'type': 'ir.actions.act_window',
            'res_model': 'hr.manager.history',
            'view_mode': 'list,form',
            'domain': [('employee_id', '=', self.id)],
            'context': {'default_employee_id': self.id},
        }



    @api.onchange('department_id')
    def _onchange_department_id_set_manager(self):
        """Automatically set manager from department."""
        for rec in self:
            if rec.department_id and rec.department_id.manager_id:
                # Auto-assign department manager
                rec.parent_id = rec.department_id.manager_id
            else:
                # No manager on department → allow manual selection
                rec.parent_id = False





