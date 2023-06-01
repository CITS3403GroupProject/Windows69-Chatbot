function toggleContainer() {
  // Get references to the necessary elements
  var leftContainer = document.getElementById("left-container");
  var toggleButton = document.getElementById("toggle-button");

  // Check the current width of the left container
  if (leftContainer.style.width === "0px") {
    // If the width is 0px, expand the container and update the toggle button text
    leftContainer.style.width = "200px";
    toggleButton.innerText = "<";
  } else {
    // If the width is not 0px, collapse the container and update the toggle button text
    leftContainer.style.width = "0px";
    toggleButton.innerText = ">";
  }

  // Toggle the display property of each child element within the left container
  Array.from(leftContainer.children).forEach(function (element) {
    element.style.display = (element.style.display === "block") ? "none" : "block";
  });

  // Play a notification sound
  var audio = new Audio('../static/Src/sounds/Chimes.mp3');
  audio.play();
}




function checkScreenWidth() {
  // Get the current screen width
  var screenWidth = window.innerWidth;
  var leftContainer = document.getElementById("left-container");
  var toggleButton = document.getElementById("toggle-button");

  // Adjust the container and toggle button based on the screen width
  if (screenWidth < 768) {
    // If the screen width is less than 768px, collapse the container and update the toggle button text
    leftContainer.style.width = "0px";
    toggleButton.innerText = ">";

    // Hide all child elements within the left container
    Array.from(leftContainer.children).forEach(function (element) {
      element.style.display = "none";
    });
  } else {
    // If the screen width is 768px or greater, expand the container and update the toggle button text
    leftContainer.style.width = "200px";
    toggleButton.innerText = "<";

    // Show all child elements within the left container
    Array.from(leftContainer.children).forEach(function (element) {
      element.style.display = "block";
    });
  }
}

  

// Event listener for the "load" event
window.addEventListener("load", checkScreenWidth);

// Event listener for the "resize" event
window.addEventListener("resize", checkScreenWidth);





function openbotpopup() {

  document.getElementById("addbotpopup").style.display = "block";
  document.getElementById("overlay").style.display = "block";


  var audio = new Audio('../static/Src/sounds/Ding.mp3'); 
  audio.play();

}



function closebotpopup() {
  document.getElementById("addbotpopup").style.display = "none";
  document.getElementById("overlay").style.display = "none";
  $("#bot_name")[0].value = ""
  $("#bot_begin_prompt")[0].value = ""
  $("#submit_bot").text("Submit")

  var audio = new Audio('../static/Src/sounds/Ding.mp3'); 
  audio.play();
}
