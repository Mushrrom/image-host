var loginBox = document.getElementById("login-box");
var signupBox = document.getElementById("signup-box");
signupBox.style.display = "none";
loginBox.style.display = "none";

var login_button = document.getElementById("login_btn");


document.getElementById("login_btn").onclick = login_func;

function login_func() {
  console.log("aaaa")
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
  console.log("bbbbb")
  console.log(signupBox.style.display)
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
