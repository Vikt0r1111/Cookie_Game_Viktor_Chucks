/* ============================================ */
/* REGISTRATION FORM VALIDATION                */
/* ============================================ */

const form = document.getElementById('registrationForm');
const usernameInput = document.getElementById('username');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const confirmPasswordInput = document.getElementById('confirmPassword');
const termsCheckbox = document.getElementById('terms');
const passwordErrorMessage = document.getElementById('passwordError');

/* ============================================ */
/* Validate Email Function */
/* ============================================ */

function setlanguage() {
  const userlang = navigator.language
  termsbutton = document.getElementById("termslink").href="/privacy-policy/" + userlang
    
}
setlanguage()

function validateEmail(email) {
  // Simple email validation regex
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

/* ============================================ */
/* Check if Passwords Match - Real-time Feedback */
/* ============================================ */

function checkPasswordsMatch() {
  const password = passwordInput.value;
  const confirmPassword = confirmPasswordInput.value;

  // Don't show message if confirm password is empty
  if (confirmPassword === '') {
    passwordErrorMessage.style.display = 'none';
    confirmPasswordInput.style.borderColor = '';
    return false;
  }

  // Check if passwords match
  if (password === confirmPassword && password !== '') {
    // Passwords match - show success
    passwordErrorMessage.style.display = 'block';
    passwordErrorMessage.textContent = '✓ Passwords match';
    passwordErrorMessage.style.color = 'green';
    confirmPasswordInput.style.borderColor = 'green';
    return true;
  } else {
    // Passwords don't match - show error
    passwordErrorMessage.style.display = 'block';
    passwordErrorMessage.textContent = '✗ Passwords do not match';
    passwordErrorMessage.style.color = 'red';
    confirmPasswordInput.style.borderColor = 'red';
    return false;
  }
}

/* ============================================ */
/* Validate Password Strength */
/* ============================================ */

function validatePasswordStrength(password) {
  const minLength = 12; // Minimum 12 characters
  const hasUpperCase = /[A-Z]/.test(password);
  const hasNumber = /\d/.test(password);
  const hasSpecialChar = /[!@#$%^&*]/.test(password);

  return (
    password.length >= minLength && hasUpperCase && hasNumber && hasSpecialChar
  );
}

/* ============================================ */
/* Validate Entire Form on Submit */
/* ============================================ */

function validateForm(event) {
  let isValid = true;

  // Check username
  if (usernameInput.value.trim() === '') {
    isValid = false;
    alert('Username is required');
  }

  // Check email
  if (!validateEmail(emailInput.value)) {
    isValid = false;
    alert('Please enter a valid email address');
  }

  // Check password strength
  if (!validatePasswordStrength(passwordInput.value)) {
    isValid = false;
    alert(
      'Password must be at least 12 characters with uppercase, number, and special character'
    );
  }

  // Check if passwords match
  if (!checkPasswordsMatch()) {
    isValid = false;
    alert('Passwords do not match');
  }

  // Check terms
  if (!termsCheckbox.checked) {
    isValid = false;
    alert('You must agree to the Terms & Conditions');
  }

  // Prevent form submission if invalid
  if (!isValid) {
    event.preventDefault();
  }

  return isValid;
}

/* ============================================ */
/* Event Listeners */
/* ============================================ */

// Real-time password match checking
confirmPasswordInput.addEventListener('input', function () {
  checkPasswordsMatch();
});

// Also check when password field changes
passwordInput.addEventListener('input', function () {
  if (confirmPasswordInput.value !== '') {
    checkPasswordsMatch();
  }
});

// Form submission validation
form.addEventListener('submit', function (event) {
  validateForm(event);
});

