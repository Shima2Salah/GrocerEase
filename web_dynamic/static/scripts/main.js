// Add JS here
// Example starter JavaScript for disabling form submissions if there are invalid fields
(() => {
    'use strict'
  
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    const forms = document.querySelectorAll('.needs-validation')
  
    // Loop over them and prevent submission
    Array.from(forms).forEach(form => {
      form.addEventListener('submit', event => {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }
  
        form.classList.add('was-validated')
      }, false)
    })
  })()
  
function stepAmount(inputId, stepValue) {
    const input = document.getElementById(inputId);
    let currentAmount = parseFloat(input.value) || 0;
    let newAmount = currentAmount + stepValue;
        
    // Ensure newAmount is not below the minimum value
    if (newAmount < parseFloat(input.min)) {
        newAmount = parseFloat(input.min);
    }
        
    input.value = newAmount.toFixed(2);
}
