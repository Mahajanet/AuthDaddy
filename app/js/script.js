const registrationForm = document.getElementById("reg-form");
const passwordInput = document.getElementById("password");
const confirmPasswordInput = document.getElementById("confirmpassword");
const errorElement = document.getElementById("error");
const firstform = document.getElementById("firstform")
const secondform = document.getElementById("secondform")

function accessPassword(password){
    return password.value;
}

var fix_password;
// Registeration form code for submision
registrationForm.addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent form submission

    const username = registrationForm.username.value;
    const password = passwordInput.value;
    fix_password = password;
    
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
        secondform.style.height = "100%";
        secondform.style.width = "100%";
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
//
//
//
//
//
const counterSpan = document.getElementById("counter");
const bioForm = document.getElementById("bio-form");
const submitButton = document.getElementById("submit-bio");
const messageElement = document.getElementById("message");
const textInput = document.getElementById("passwordVerify");
let counterValue = parseInt(counterSpan.textContent);


// Function to decrement the counter value and handle the message and button removal
function decrementCounter() {
    if (counterValue === 1) {
        secondform.style.display = "none";

    }
    counterValue--;
    counterSpan.textContent = counterValue;
}

// Event listener for form submission
bioForm.addEventListener("submit", function (event) {;

    event.preventDefault(); // Prevent form submission
    const new_password = textInput.value;

    if (fix_password !== new_password) {
        messageElement.style.color = "red";
        showMessage("Entry doesn't match the password you set. Please try again!");
        clearField(); 
    } else{
        decrementCounter();
        messageElement.style.color = "green";
        showMessage("That's valid!");
        clearField();
    }
});

function showMessage(message) {
    messageElement.textContent = message;
}

// Function to clear the input field
function clearField() {
    textInput.value = '';
}
