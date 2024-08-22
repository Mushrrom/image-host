var loginBox = document.getElementById("login-box");
var signupBox = document.getElementById("signup-box");
signupBox.style.display = "none";
loginBox.style.display = "none";
signUpUsername = document.getElementById("username_signup");
signUpPassword = document.getElementById("password_signup");
logInUsername = document.getElementById("username_login");
logInPassword = document.getElementById("password_login");

var login_button = document.getElementById("login_btn");

// document.getElementById("login_btn").onclick = login_func;

function login_func() {
    console.log("aaaa");
    if (loginBox.style.display === "none") {
        loginBox.style.display = "block";
        login_button.style.backgroundColor = "#bababd";
    } else {
        loginBox.style.display = "none";
        login_button.style.backgroundColor = "#e9e9ed";
    }
    if (signupBox.style.display === "block") {
        signupBox.style.display = "none";
        signup_button.style.backgroundColor = "#e9e9ed";
    }
}

var signup_button = document.getElementById("signup_btn");

document.getElementById("signup_btn").onclick = signup_func;

function signup_func() {
    console.log("bbbbb");
    console.log(signupBox.style.display);
    if (signupBox.style.display === "none") {
        signupBox.style.display = "block";
        signup_button.style.backgroundColor = "#bababd";
    } else {
        signupBox.style.display = "none";
        signup_button.style.backgroundColor = "#e9e9ed";
    }
    if (loginBox.style.display === "block") {
        loginBox.style.display = "none";
        login_button.style.backgroundColor = "#e9e9ed";
    }
}

async function submit_sign_up() {
    console.log(signUpUsername.value);
    console.log(signUpPassword.value);

    const formData = new FormData();

    // Add a text field
    formData.append("username", signUpUsername.value);
    formData.append("password", signUpPassword.value);
}

async function submit_login() {
    console.log(logInUsername.value);
    console.log(logInPassword.value);

    const formData = new FormData();

    // Add a text field
    formData.append("username", logInUsername.value);
    formData.append("password", logInPassword.value);

    const response = await fetch("/api/login", {
        method: "POST",
        // Set the FormData instance as the request body
        body: formData,
    });

    // console.log(await response.json());
    // response = await response.json();
    // console.log(await )
    response_json = await response.json();
    if ((await response_json.success) === 0) {
        console.log("avc");
        alert(response_json.error);
    } else {
        document.cookie = `session_key=${response.session_key}; expires=Thu, 18 Dec 2999 12:00:00 UTC; path=/`;
        alert("successfully logged in");
    }

    window.location.href = "/"
}
