const storedUser = {username:"admin", password:"@Dm1n"};

function login(){
  const u = document.getElementById('username').value;
  const p = document.getElementById('password').value;
  if(u===storedUser.username && p===storedUser.password){
    document.getElementById('loginPage').style.display="none";
    document.getElementById('app').classList.remove("hidden");
    document.getElementById('userInitials').innerText = u.slice(0,2).toUpperCase();
    showPage("cameras");
  } else {
    document.getElementById('loginError').innerText="Invalid credentials";
  }
}

function logout(){ location.reload(); }

function showPage(id){
  document.querySelectorAll(".page").forEach(p => p.classList.add("hidden"));
  document.getElementById(id).classList.remove("hidden");
}

/* Validation */
function validateEmail(){
  const v = document.getElementById('email').value;
  if(v===""){ document.getElementById('emailError').innerText="Email is required"; return false;}
  const valid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);
  document.getElementById('emailError').innerText = valid ? "" : "Email must follow example@mail.com";
  return valid;
}

function validatePhone(){
  const v = document.getElementById('phone').value;
  if(v===""){ document.getElementById('phoneError').innerText="Phone is required"; return false;}
  const valid = /^\+?[0-9\s]{7,15}$/.test(v);
  document.getElementById('phoneError').innerText = valid ? "" : "Phone must contain 7-15 digits";
  return valid;
}

function submitForm(e){
  e.preventDefault();
  const name = document.getElementById('name').value.trim();
  if(name===""){ document.getElementById('nameError').innerText="Name is required"; } 
  else { document.getElementById('nameError').innerText=""; }

  const emailValid = validateEmail();
  const phoneValid = validatePhone();

  if(name && emailValid && phoneValid){
    document.getElementById('formSuccess').innerText="Message sent successfully!";
  } else {
    document.getElementById('formSuccess').innerText="";
  }

  const form = document.getElementById('myForm');

  form.addEventListener('submit', function(event) {
    event.preventDefault();
    alert('Form submitted!');
  });
}
