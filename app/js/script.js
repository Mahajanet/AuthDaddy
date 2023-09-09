const registrationForm = document.getElementById("reg-form");
const passwordInput = document.getElementById("password");
const confirmPasswordInput = document.getElementById("confirmpassword");
const errorElement = document.getElementById("error");
const firstform = document.getElementById("firstform")
const secondform = document.getElementById("secondform")

// Registeration form code for submision
registrationForm.addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent form submission

    const username = registrationForm.username.value;
    const password = passwordInput.value;
    const confirmPassword = confirmPasswordInput.value;

    // Password validation criteria
    const passwordRegex = /^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;

    if (password !== confirmPassword) {
        showError("Passwords do not match. Please try again.");
        clearFields();
    } else if (!password.match(passwordRegex)) {
        showError("Password must be at least 8 characters long, and contain at least one uppercase letter, one number, and one special character (@$!%*?&).");
        clearFields();
    } else {
        // Registration successful, you can send the data to the server or perform further actions here
        errorElement.textContent = "";
        //hides the first form to replace with biometrics 
        firstform.style.display = "none";
        //shows the second form that displays the biometrics
        secondform.style.display = "block";
        // Clear form inputs
        registrationForm.reset();
    }
});

function showError(message) {
    errorElement.textContent = message;
}

function clearFields() {
    passwordInput.value = '';
    confirmPasswordInput.value = '';
}

//Type Habits form code submission 