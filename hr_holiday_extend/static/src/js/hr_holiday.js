odoo.define("hr_holiday_extend.payslip.tree.extend", function (require) {
    "use strict";

    var PayslipListController = require("hr_payroll.payslip.tree");
    var PayslipFormController = require("hr_payroll_holidays.payslip.form");

    PayslipListController.include({
        _displayWarning: function ($warning) {
            console.log("PayslipListController..._displayWarning...")
            setTimeout(function() {
                this.$('.o_list_view').before($warning);
            },500)
        },
    });

    PayslipFormController.include({
        _displayWarning: function ($warning) {
            console.log("PayslipFormController..._displayWarning...")
            setTimeout(function() {
                this.$('.o_form_statusbar').after($warning);
            },500)
        },
    });

});