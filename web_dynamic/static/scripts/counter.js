document.addEventListener('DOMContentLoaded', function() {
    const amountInput = document.getElementById('amount');
    const minOrderAmount = parseFloat(amountInput.min);

    // Ensure the input value is a number
    amountInput.value = parseFloat(amountInput.value) || minOrderAmount;

    document.getElementById('increase').addEventListener('click', function() {
        let currentAmount = parseFloat(amountInput.value);
        if (isNaN(currentAmount)) {
            currentAmount = minOrderAmount;
        }
        let newAmount = currentAmount + minOrderAmount;
        amountInput.value = newAmount.toFixed(2); // Set value with two decimal places
    });

    document.getElementById('decrease').addEventListener('click', function() {
        let currentAmount = parseFloat(amountInput.value);
        if (isNaN(currentAmount)) {
            currentAmount = minOrderAmount;
        }
        let newAmount = Math.max(minOrderAmount, currentAmount - minOrderAmount);
        amountInput.value = newAmount.toFixed(2); // Set value with two decimal places
    });
});
