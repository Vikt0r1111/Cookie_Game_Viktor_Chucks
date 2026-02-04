/* ============================================ */
/* HOME.JS - Home Page JavaScript              */
/* ============================================ */

/* TODO: Get necessary DOM elements */
/* Hint: Use document.getElementById() or querySelector() */

/* TODO: Load user data and display greeting */
/* Hint: Get user info from localStorage or session */
/* Hint: Update the user-greeting element with user's name */

/* TODO: Check if user is logged in */
/* Hint: Check localStorage or session for user data */

/* TODO: If not logged in, redirect to login page */
/* Hint: Use window.location.href to redirect */

/* TODO: Get and display user information */
/* Hint: Update greeting with user's name or email */

/* TODO: Check if a saved game exists */
/* Hint: Check localStorage for game save data */
/* Hint: Enable or disable the continue button based on save data */

/* TODO: Add event listener to "New Game" button */
/* Hint: Use addEventListener("click", function) */

/* TODO: Clear any existing game state from localStorage */
/* Hint: Use localStorage.removeItem() or clear specific game data */

/* TODO: Redirect to game page */
/* Hint: Use window.location.href = "game.html" */

/* TODO: Add event listener to "Continue Game" button */
/* Hint: Use addEventListener("click", function) */

/* TODO: Load game state from localStorage */
/* Hint: Use localStorage.getItem('gameState') */

/* TODO: Verify the saved game data is valid */
/* Hint: Parse and validate the game state */

/* TODO: Redirect to game page */
/* Hint: The game page should load the saved state */

/* TODO: Add event listener to logout button */
/* Hint: Use addEventListener("click", function) */

/* TODO: Confirm logout action */
/* Hint: Use confirm() to ask user if they want to logout */

/* TODO: Clear user session/localStorage */
/* Hint: Use localStorage.clear() or remove specific user data */

/* TODO: Redirect to login page */
/* Hint: Use window.location.href = "login.html" */

/* TODO: Add event listeners for register button if needed */
/* Hint: Get the register link and add navigation */

/* TODO: Add welcome animation */
/* Hint: Add CSS animation classes on page load */

/* TODO: Implement auto-logout after inactivity */
/* Hint: Track user activity and logout after certain timeout */
      // Popup logic
      const accountIcon = document.getElementById("account-icon");
      const accountPopup = document.getElementById("account-popup");
      accountIcon.onclick = () => {
          accountPopup.style.display = accountPopup.style.display === "block" ? "none" : "block";
      };

      document.addEventListener("click", (e) => {
          if (!accountIcon.contains(e.target) && !accountPopup.contains(e.target)) {
              accountPopup.style.display = "none";
          }
      });

      document.getElementById('popup-logout-btn').addEventListener('click', async () => {
          const response = await fetch('/logout', { method: 'POST' });

          window.location.href = '/login';
      });