odoo.define('ak_library_management.customer_fetch', function (require) {
    "use strict";

    var ajax = require('web.ajax');
    $(document).ready(function () {
        $('#fetch_customer').click(function () {
            var email = $('#customer_email').val();
            if (!email) {
                alert("Please enter an email.");
                return;
            }

            ajax.jsonRpc('/customer/details', 'call', { email: email }).then(function (data) {
                if (data.error) {
                    $('#customer_info').html(`<p style="color:red;">${data.error}</p>`);
                } else {
                    $('#customer_info').html(`
                        <p><strong>Name:</strong> ${data.name}</p>
                        <p><strong>Email:</strong> ${data.email}</p>
                        <p><strong>Phone:</strong> ${data.phone}</p>
                        <p><strong>Company:</strong> ${data.company}</p>
                    `);
                }
            });
        });
    });
});