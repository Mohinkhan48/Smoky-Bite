(function ($) {
    $(document).ready(function () {
        let menuPrices = {};

        // Fetch menu prices once when page loads
        fetch('/api/menu_prices/')
            .then(response => response.json())
            .then(data => {
                menuPrices = data;
                console.log("Menu prices loaded:", menuPrices);
            });

        function calculateTotal() {
            let total = 0;
            // Iterate over each visible row in the tabular inline
            $('.dynamic-items').each(function () {
                const menuItemId = $(this).find('select[name$="-menu_item"]').val();
                const quantity = parseInt($(this).find('input[name$="-quantity"]').val()) || 0;

                if (menuItemId && menuPrices[menuItemId]) {
                    const price = menuPrices[menuItemId];
                    const rowPriceField = $(this).find('.field-price p');

                    // Update the price display in the row (if it's a readonly field)
                    if (rowPriceField.length) {
                        rowPriceField.text(price.toFixed(2));
                    }

                    total += price * quantity;
                }
            });

            // Update the total_amount field (now an input)
            $('#id_total_amount').val(total.toFixed(2));
        }

        // Listen for changes on menu items and quantities
        $(document).on('change', 'select[name$="-menu_item"], input[name$="-quantity"]', function () {
            calculateTotal();
        });

        // Also handle added rows
        $(document).on('formset:added', function (event, $row, formsetName) {
            calculateTotal();
        });

        // --- POS List View Row Highlighting ---
        function highlightRows() {
            $('.results tbody tr').each(function () {
                const $row = $(this);
                const paymentStatus = $row.find('.field-pay_status span').text().trim();
                const orderStatus = $row.find('.field-order_status span').text().trim();

                // Highlight PENDING orders and bills
                if (paymentStatus === 'PENDING' || orderStatus === 'PENDING') {
                    $row.addClass('row-pending');
                } else if (paymentStatus === 'PAID') {
                    $row.addClass('row-paid');
                }
            });
        }

        // Run on list pages
        if ($('.results').length) {
            highlightRows();
        }
    });
})(django.jQuery);
