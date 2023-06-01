// Function to minimize windows
function Minimize() {
  // Get all elements with class "window-popout"
  var containerDivs = document.getElementsByClassName("window-popout");

  // Loop through each containerDiv
  for (var i = 0; i < containerDivs.length; i++) {
    // Check if the display property is "none"
    if (containerDivs[i].style.display === "none") {
      // If it is "none", change it to "flex" to display the window
      containerDivs[i].style.display = "flex";
    } else {
      // If it is not "none", change it to "none" to hide the window
      containerDivs[i].style.display = "none";
    }
  }

  // Create an audio object with the Notify.mp3 file path
  var audio = new Audio("../static/Src/sounds/Recycle.mp3");
  // Play the audio
  audio.play();
}

// Function to close the app
function closeAPP() {
  // Get all elements with class "window-popout"
  var containerDivs = document.getElementsByClassName("window-popout");

  // Loop through each containerDiv
  for (var i = 0; i < containerDivs.length; i++) {
    // Hide the window by setting its display property to "none"
    containerDivs[i].style.display = "none";
  }

  // Hide the button with ID "windows69APP" by setting its display property to "none"
  var button = document.getElementById("windows69APP");
  button.style.display = "none";

  // Create an audio object with the Shutdown.mp3 file path
  var audio = new Audio("../static/Src/sounds/Shutdown.mp3");
  // Play the audio
  audio.play();
}

// Function to open the app
function openAPP() {
  var containerDivs = document.getElementsByClassName("window-popout");

  // Iterate through each container div
  for (var i = 0; i < containerDivs.length; i++) {
    if (containerDivs[i].style.display === "none") {
      containerDivs[i].style.display = "flex";
    } else {
      containerDivs[i].style.display = "flex";
    }
  }

  var button = document.getElementById("windows69APP");
  button.style.display = "none";

  // Toggle the display property of the button
  if (button.style.display === "none") {
    button.style.display = "flex";
  } else {
    button.style.display = "none";
  }

  document.getElementById("popup").style.display = "flex";
  document.getElementById("overlay").style.display = "flex";

  var audio = new Audio("../static/Src/sounds/Start-up.mp3");
  audio.play();
}

// Function to close the popup
function closePopup() {
  document.getElementById("popup").style.display = "none";
  document.getElementById("overlay").style.display = "none";

  var audio = new Audio("../static/Src/sounds/Tada.mp3");
  audio.play();
}

// Add additional content to the content div
var contentDiv = document.getElementById("content");
for (var i = 0; i < 50; i++) {
  var channel = document.createElement("li");
  channel.innerText = "Additional content " + (i + 1);
  contentDiv.appendChild(channel);
}

// Function to open a sub-popup
function opensubpopup() {
  // Display the addchannelpopup element
  document.getElementById("addchannelpopup").style.display = "block";
  // Display the overlay element
  document.getElementById("overlay").style.display = "block";

  // Create a new audio object with the Ding.mp3 sound file
  var audio = new Audio("../static/Src/sounds/Ding.mp3");
  // Play the audio
  audio.play();
}

// Function to close the sub-popup
function closesubpopup() {
  // Hide the addchannelpopup element
  document.getElementById("addchannelpopup").style.display = "none";
  // Hide the overlay element
  document.getElementById("overlay").style.display = "none";
  document.getElementById("channel_name").value = "";

  // Create a new audio object with the Ding.mp3 sound file
  var audio = new Audio("../static/Src/sounds/Ding.mp3");
  // Play the audio
  audio.play();
}

// Function to open a sub-popup
function opensearchpopup() {
  document.getElementById("searchPopup").style.display = "block";
  document.getElementById("overlay").style.display = "block";

  // Create a new audio object with the Ding.mp3 sound file
  var audio = new Audio("../static/Src/sounds/Ding.mp3");
  // Play the audio
  audio.play();
}

// Function to close the sub-popup
function closesearchpopup() {
  document.getElementById("searchPopup").style.display = "none";
  // Hide the overlay element
  document.getElementById("overlay").style.display = "none";
  document.getElementById("search-query").text = "";

  // Create a new audio object with the Ding.mp3 sound file
  var audio = new Audio("../static/Src/sounds/Ding.mp3");
  // Play the audio
  audio.play();
}

function Adduser() {
  document.getElementById("addUserpop").style.display = "flex";
  document.getElementById("overlay").style.display = "flex";
}

function closeAdduser() {
  document.getElementById("addUserpop").style.display = "none";
  document.getElementById("overlay").style.display = "none";
}

function Viewuser() {
  document.getElementById("seeusers").style.display = "flex";
  document.getElementById("overlay").style.display = "flex";
}

function closeViewuser() {
  document.getElementById("seeusers").style.display = "none";
  document.getElementById("overlay").style.display = "none";
}




document.addEventListener("DOMContentLoaded", function() {
  // Check if the message has already been displayed
  if (localStorage.getItem("messageDisplayed")) {
    document.getElementById("popup").style.display = "none";
    document.getElementById("overlay").style.display = "none";
  } else {
    // Display the message
    document.getElementById("popup").style.display = "flex";
    document.getElementById("overlay").style.display = "flex";

    // Set the flag to indicate that the message has been displayed
    localStorage.setItem("messageDisplayed", true);
  }
});



function openinstructions() {
  document.getElementById("Instructions").style.display = "flex";
  document.getElementById("overlay").style.display = "flex";
}


function closeinstructions() {
  document.getElementById("Instructions").style.display = "none";
  document.getElementById("overlay").style.display = "none";
}