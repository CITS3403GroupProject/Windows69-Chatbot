
document.addEventListener("DOMContentLoaded", function () {

  const form = document.querySelector("#login-form");
  const emailInput = document.querySelector("#email");
  const passwordInput = document.querySelector("#password");
  const loginError = document.querySelector("#login-error");

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = new FormData();
    formData.append("email", emailInput.value);
    formData.append("password", passwordInput.value);

    try {
      const response = await fetch("/api/v1/auth/login", {
        method: "POST",
        body: formData,
      });
      const responseData = await response.json();

      // Reset errors
      loginError.style.visibility = "hidden";
      emailInput.classList.remove("is-invalid");
      passwordInput.classList.remove("is-invalid");

      if (response.ok) {
        window.location.replace("/");
      } else if (responseData.error) {
        // .. and add back errors if any encountered.
        loginError.style.visibility = "visible";
        loginError.textContent = responseData.message;
        emailInput.classList.add("is-invalid");
        passwordInput.classList.add("is-invalid");
      }
    } catch (error) {
      console.error(error);
    }
  });
});

