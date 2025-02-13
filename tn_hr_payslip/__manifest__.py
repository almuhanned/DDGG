{
    "name": "Telenoc HR Payslip",
    "description": """
        Telenoc HR Payslip
    """,
    "author": "Sary Babiker",
    "category": "hr",
   'version': '15.0.1.0',
    "depends": ['hr', 'hr_payroll', 'tn_hr_annual_leave_auto_allocation', 'hr_contract_updation', 'telenoc_hr_employee_updation', 'hr_annual_leave_allocation', 'hr_annual_leave_payslip','account'],
    "data": [
        'security/security.xml',
        "reports/report_payslip_inherit.xml",
        # 'views/hr_employee_view.xml',
        'views/hr_payslips_view.xml',
	    # 'views/end_of_service_award_view.xml',
        'views/hr_payrol_structure_view.xml',
        'views/hr_leave_view.xml',
        'views/account_move_view.xml'
    ],
}
