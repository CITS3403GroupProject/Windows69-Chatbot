window.addEventListener('DOMContentLoaded', function () {
  // Get the container element
  var container = document.querySelector('.container');

  // Add event listener for the mousedown event on the container
  container.addEventListener('mousedown', initResize, false);

  // Set the minimum width and height limits
  var minWidth = 700;
  var minHeight = 700;

  var startX, startY, startWidth, startHeight;

  function initResize(e) {
    // Store the initial mouse coordinates and container dimensions
    startX = e.clientX;
    startY = e.clientY;
    startWidth = parseInt(document.defaultView.getComputedStyle(container).width, 10);
    startHeight = parseInt(document.defaultView.getComputedStyle(container).height, 10);

    // Add event listeners for mousemove and mouseup events on the window
    window.addEventListener('mousemove', resize, false);
    window.addEventListener('mouseup', stopResize, false);
  }

  function resize(e) {
    // Calculate the new dimensions based on the mouse movement
    var newWidth = startWidth + e.clientX - startX;
    var newHeight = startHeight + e.clientY - startY;

    // Check if the new dimensions exceed the minimum limits and update the container size
    if (newWidth > minWidth) {
      container.style.width = newWidth + 'px';
    }
    if (newHeight > minHeight) {
      container.style.height = newHeight + 'px';
    }
  }

  function stopResize(e) {
    // Remove the event listeners for mousemove and mouseup events on the window
    window.removeEventListener('mousemove', resize, false);
    window.removeEventListener('mouseup', stopResize, false);
  }
});
