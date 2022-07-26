odoo.define('gst_eminis_pos.models', function (require) {
    'use strict';

    const models = require('point_of_sale.models');
    models.load_fields('product.product', 'changed_price');
});