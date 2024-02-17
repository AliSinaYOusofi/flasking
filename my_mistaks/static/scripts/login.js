const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");
const svg_close_button = document.getElementById("svg_close_button")
let message_div = document.getElementById("message_div")
let message_text = document.getElementById("message_text")
let loader = document.getElementById("loader")
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
  loader.style.display = 'block'
  try {
    message_div.style.display = 'none'
    const response = await fetch("http://127.0.0.1:5000/auth/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ email: email.value, password: password.value })
    })
    const data = await response.json();
    
    if (data.message === "User not found") {
      message_text.innerHTML = "User not found"
      message_div.style.display = "flex"
      message_div.classList.add("error-message")
    }

    else if (data.message === "emailOrPasswordIncorrect") {
      
      message_text.innerHTML = "Email or password incorrect"
      message_div.style.display = "flex"
      message_div.classList.add("error-message")
    }

    else if (data.message === "error") {
      let error_message_container = document.getElementById("message")

      message_text.innerHTML = "Server error happened"
      
      message_div.style.display = "block"
      message_div.classList.add("error-message")
    }

    else if (data.message === "success") {
      localStorage.setItem("session_id", data.session_id)
      window.location.href = "/main"
    }
  } catch(e) {
    console.error("error", e)
    message_text.innerHTML = "Server error happened"
      
    message_div.style.display = "block"
    message_text.style.textAlign = "center"
    message_div.classList.add("error-message")
  } finally {
    loader.style.display = 'none'
  }
})


svg_close_button.addEventListener("click", function () {
  message_div.style.display = 'none'
})