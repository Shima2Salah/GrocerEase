// Function to increment the quantity
function increment() {
    var quantityInput = document.getElementById('quantity');
    var quantity = parseInt(quantityInput.value);
    if (quantity < 10) {
        quantityInput.value = quantity + 1;
    }
}

// Function to decrement the quantity
function decrement() {
    var quantityInput = document.getElementById('quantity');
    var quantity = parseInt(quantityInput.value);
    if (quantity > 1) {
        quantityInput.value = quantity - 1;
    }
}
