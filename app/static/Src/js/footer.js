// Window controls
var mainWindow = document.getElementById("mainWindow");
var mainBtn = document.getElementById("mainBtn");
var isOpen = true;

function minimise() {
  mainWindow.style.display =
    mainWindow.style.display === "none" ? "block" : "none";
  mainBtn.classList.add("btn-invis");
}

function closeWindow() {
  minimise();
  isOpen = false;
  var audio = new Audio("../static/Src/sounds/Notify.mp3");
  audio.play();
}

function openWindow() {
  if (isOpen === false) {
    mainBtn.classList.remove("btn-invis");
    mainWindow.style.display = "block";
    isOpen = true;
  } else {
    minimise();
    isOpen = false;
  }
  var audio = new Audio("../static/Src/sounds/Notify.mp3");
  audio.play();
}

// Footer clock
function updateTime() {
  var date = new Date();
  var hours = date.getHours();
  var minutes = date.getMinutes();

  hours = hours < 10 ? "0" + hours : hours;
  minutes = minutes < 10 ? "0" + minutes : minutes;

  var time = hours + ":" + minutes;

  document.getElementById("time").innerHTML = time;
}
// Update every second
setInterval(updateTime, 1000);

function toggleStartMenu() {
  var menu = document.getElementById("startMenu");
  menu.style.display = menu.style.display === "block" ? "none" : "block";
  var audio = new Audio("../static/Src/sounds/Notify.mp3");
  audio.play();
}

/**
 * Logs out the user.
 */
function logOut() {
  var audio = new Audio("../static/Src/sounds/Shutdown.mp3");
  audio.play();

  // Display overlay and shutdown elements
  document.getElementById("overlay").style.display = "block";
  document.getElementById("shutdown").style.display = "block";

  // Delay logout action for 7 seconds
  setTimeout(function () {
    // Perform logout action here
    window.location.href = "/logout";
  }, 7000);
}
