odoo.define('gst_eminis_pos.PrintTagsButton', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const Registries = require('point_of_sale.Registries');
    const Dialog = require('web.Dialog');
    const core = require('web.core');
    const { useListener } = require('web.custom_hooks');

    var _t = core._t;

    class PrintTagsButton extends PosComponent {
        constructor() {
            super(...arguments);
            useListener('click', this.onClick);
        }
        async onClick() {
            showAlert(_t("Sending download request..."));
            var url = "/pos/product_template_label_eminis_report/download?";
            var link = window.document.createElement('a');
            link.href = url;
            link.download = '';
            link.click();
        }
    }

    PrintTagsButton.template = 'PrintTagsButton';

    ////////////////////////////////////////////////////
    // BEGIN ALERT BOX
    ////////////////////////////////////////////////////
    var timer;
    var ActiveElement;
    var actionAlert;
    function showAlert(message, action=false) {
        actionAlert = action;
        clearTimeout(timer);
        ActiveElement = document.activeElement;
        $(".message_text").html(message);
        $("div.alert_box").removeClass("hidden");
        timer = setTimeout(function() {
            closeAlert();
        }, 3000);
    }
    function closeAlert() {
        $("div.alert_box").addClass("hidden");
        clearTimeout(timer);
        if (ActiveElement) {
            ActiveElement.focus();
        }
        if (actionAlert) {
            actionAlert();
        }
    }
    ////////////////////////////////////////////////////
    // END ALERT BOX
    ////////////////////////////////////////////////////

    ProductScreen.addControlButton({
        component: PrintTagsButton,
        condition: () => true,
        position: ['after', 'SetSaleOrderButton'],
    });

    Registries.Component.add(PrintTagsButton);

    return PrintTagsButton;
});

