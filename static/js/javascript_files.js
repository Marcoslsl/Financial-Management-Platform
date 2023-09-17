document.getElementById("add-new-purchase-btn").addEventListener("click", function () {
        var newPurchaseForm = document.getElementById("new-purchase-form");
        if (newPurchaseForm.style.display === "none" || newPurchaseForm.style.display === "") {
            newPurchaseForm.style.display = "block";
        } else {
            newPurchaseForm.style.display = "none";
        }
    });

document.addEventListener('DOMContentLoaded', function() {
        const deleteButtons = document.querySelectorAll('.btn-danger');

        deleteButtons.forEach(function(button) {
            button.addEventListener('click', function(event) {
                const confirmMessage = button.getAttribute('data-confirm');
                if (!confirm(confirmMessage)) {
                    event.preventDefault(); 
                }
            });
        });
    });