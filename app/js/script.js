const counterSpan = document.getElementById("counter");
const counterForm = document.getElementById("form");
const submitButton = document.getElementById("submit");
const messageElement = document.getElementById("message");
const textInput = document.getElementById("password");
let counterValue = parseInt(counterSpan.textContent);

// Function to decrement the counter value and handle the message and button removal
function decrementCounter() {
    counterValue--;
    counterSpan.textContent = counterValue;
    if (counterValue === 0) {
        messageElement.textContent = "Thank you";
        submitButton.style.display = "none"; // Hide the submit button
    }
    clearField();
}

// Event listener for form submission
counterForm.addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent form submission
    decrementCounter();
});

// Event listener for Enter key press in the text input field
textInput.addEventListener("keyup", function (event) {
    if (event.key === "Enter") {
        event.preventDefault(); // Prevent Enter from submitting the form
        decrementCounter();
    }
});

// Function to clear the input field
function clearField() {
    textInput.value = '';
}
