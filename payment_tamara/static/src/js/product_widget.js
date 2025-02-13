/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
odoo.define('payment_tamara_product_widget.product_widget', function (require) {
    "use strict";

    var ajax = require('web.ajax');
    var VariantMixin = require('sale.VariantMixin');

    const originalOnChangeCombination = VariantMixin._onChangeCombination;
    VariantMixin._onChangeCombination = function (ev, $parent, combination) {
        $('.tamara-summary').attr('amount', combination.price)
        window.TamaraWidgetV2.refresh();
        originalOnChangeCombination.apply(this, [ev, $parent, combination]);
    };


});

