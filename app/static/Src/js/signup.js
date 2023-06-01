document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("#signup-form");
  const emailInput = document.querySelector("#email");
  const usernameInput = document.querySelector("#username");
  const passwordInput = document.querySelector("#password");

  const errorElements = {
    username_exists: {
      msgBox: document.querySelector("#username-error"),
      inputBox: usernameInput,
    },
    email_exists: {
      msgBox: document.querySelector("#email-error"),
      inputBox: emailInput,
    },
  };

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = new FormData();
    formData.append("email", emailInput.value);
    formData.append("username", usernameInput.value);
    formData.append("password", passwordInput.value);

    try {
      const response = await fetch("/api/v1/auth/signup", {
        method: "POST",
        body: formData,
      });
      const responseData = await response.json();

      // Reset errors
      for (element in errorElements) {
        errorElements[element].msgBox.style.visibility = "hidden";
        errorElements[element].inputBox.classList.remove("is-invalid");
      }


      if (response.ok) {
        window.location.replace("/login");
      } else {
        // .. and add back errors if any encountered.
        for (error in responseData.errors) {
          errorType = responseData.errors[error].error;
          errorElements[errorType].inputBox.classList.add("is-invalid");
          errorMsgBox = errorElements[errorType].msgBox;
          errorMsgBox.textContent = responseData.errors[error].message;
          errorMsgBox.style.visibility = "visible";
        }
      }
    } catch (error) {
      console.error(error);
    }
  })
});
