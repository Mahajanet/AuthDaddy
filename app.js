const fs = require('fs');
const util = require('util');
const { Engine } = require('matlab.engine');
const readFileAsync = util.promisify(fs.readFile);

// Define the main function to run MATLAB code
async function runMain(jsonName) {
  try {
    // Read the JSON data from a file
    const jsonStr = await readFileAsync(jsonName, 'utf8');
    const jsonData = JSON.parse(jsonStr);

    // Start the MATLAB engine
    const matlab = await Engine.startMatlab();

    // Evaluate the MATLAB script with the JSON data as an argument
    const result = await matlab.eval(`weights = main(${JSON.stringify(jsonData)});`);

    // Get the 'weights' variable from MATLAB
    const weights = await result.weights;

    console.log(weights); // Output from MATLAB script

    // Close the MATLAB engine
    await matlab.quit();
  } catch (error) {
    console.error('Error:', error);
  }
}

// Run the main function with your JSON file
runMain('leokeystrokes.txt');
