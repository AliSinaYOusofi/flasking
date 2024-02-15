const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");

sign_up_btn.addEventListener("click", () => {
    container.classList.add("sign-up-mode");
});

sign_in_btn.addEventListener("click", () => {
  container.classList.remove("sign-up-mode");
});

let email = document.getElementById("username");
let password = document.getElementById("password");

let sign_in_form_button = document.getElementById("sign-in-form-button");

sign_in_form_button.addEventListener("click", async (e) => {
  e.preventDefault()

  try {
    const response = await fetch("http://127.0.0.1:5000/auth/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ email: email.value, password: password.value })
    })
    const data = await response.json();
    
    if (data.message === "User not found") {
      let error_message_container = document.getElementById("message")
      error_message_container.innerHTML = "User not found"
      error_message_container.style.color = "white"
      error_message_container.style.display = "block"
      error_message_container.style.textAlign = "center"
      error_message_container.style.marginTop = "10px"
      error_message_container.style.backgroundColor = 'red'
      error_message_container.classList.add("error-message")
    }

    else if (data.message === "emailOrPasswordIncorrect") {
      let error_message_container = document.getElementById("message")
      error_message_container.innerHTML = "Email or password incorrect"
      error_message_container.style.color = "white"
      error_message_container.style.display = "block"
      error_message_container.style.textAlign = "center"
      error_message_container.style.marginTop = "10px"
      error_message_container.style.backgroundColor = 'red'
      error_message_container.classList.add("error-message")
    }

    else if (data.message === "error") {
      let error_message_container = document.getElementById("message")
      error_message_container.innerHTML = "Server error happened"
      error_message_container.style.color = "white"
      error_message_container.style.display = "block"
      error_message_container.style.textAlign = "center"
      error_message_container.style.marginTop = "10px"
      error_message_container.style.backgroundColor = 'red'
      error_message_container.classList.add("error-message")
    }

    else if (data.message === "success") {
      localStorage.setItem("session_id", data.session_id)
      window.location.href = "/main"
    }
  } catch(e) {
    console.error("error", e)
  }
})