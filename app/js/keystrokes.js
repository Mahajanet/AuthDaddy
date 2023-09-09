let keyData = [];

let pressedKeys = {};

function getCurrentTimestamp() {
  return new Date().getTime();
}

function determineKeyType(key) {
  if (key === "CapsLock" || key === "Shift" || key === "Backspace") {
    return key;
  }
  return "Null";
}

function handleKeyDown(event) {
  const key = event.key;
  const timestamp = getCurrentTimestamp();
  const field = event.target.getAttribute("name"); // Get the field name

  if (field === "passwordVerify") {
    const keyType = determineKeyType(key);

    const keyEvent = {
      key: keyType === "Null" ? "Null" : key,
      keyType: keyType,
      timepressed: timestamp,
      timereleased: null,
    };
    keyData.push(keyEvent);

    pressedKeys[key] = keyEvent;

    console.log(`Key '${key}' (${keyType}) pressed at ${timestamp} ms`);
  }
}

function handleKeyUp(event) {
  const key = event.key;
  const timestamp = getCurrentTimestamp();

  if (event.target.getAttribute("name") === "passwordVerify") {
    if (pressedKeys[key]) {
      pressedKeys[key].timereleased = timestamp;
      delete pressedKeys[key];
    }

    console.log(`Key '${key}' released at ${timestamp} ms`);
  }
}

const passwordField = document.querySelector('input[name="passwordVerify"]');
passwordField.addEventListener("keydown", handleKeyDown);
passwordField.addEventListener("keyup", handleKeyUp);

function saveDataToFile() {
  const jsonData = JSON.stringify(keyData, null, 2);
  const blob = new Blob([jsonData], { type: "application/json" });
  const url = URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = "keypress_data.txt";
  a.click();

  keyData = [];
}

document.getElementById("bio-form").addEventListener("submit", function (e) {
  e.preventDefault();
  saveDataToFile();
});
