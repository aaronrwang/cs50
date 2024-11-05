// Function to display the entered response
function displayResponse() {
    // Get the value from the input box
    var response = document.getElementById("responseInput").value;

    // Create a new paragraph element for the response
    var responseParagraph = document.createElement("p");
    responseParagraph.textContent = response;

    // Append the new response to the existing content
    document.getElementById("responseDisplay").appendChild(responseParagraph);

    // Clear the input box for the next response
    document.getElementById("responseInput").value = "";
}
