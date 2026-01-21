/* ============================================ */
/* GAME.JS - Cookie Clicker Game JavaScript    */
/* ============================================ */

/* TODO: Initialize game state object */
/* Hint: Create an object to store game data like cookies, upgrades, etc. */
let gameState = {
  cookies: 0,
  cookiesPerClick: 1,
  cookiesPerSecond: 0,
  upgrades: [],
};

/* TODO: Get necessary DOM elements */
/* Hint: Use document.getElementById() for buttons and displays */
const cookieButton = document.getElementById('cookieButton');
const cookieCountDisplay = document.getElementById('cookieCount');
const cpsDisplay = document.getElementById('cpsDisplay');
const cpcDisplay = document.getElementById('cpcDisplay');
const shopContainer = document.getElementById('shopContainer');
const saveButton = document.getElementById('saveButton');
const loadButton = document.getElementById('loadButton');
const backButton = document.getElementById('backButton');

/* ============================================ */
/* Initialize Game on Page Load */
/* ============================================ */

/* TODO: Initialize the game on page load */
/* Hint: Load saved game or start fresh */
window.onload = function () {
  /* TODO: Check if a saved game exists */
  /* Hint: Check localStorage for gameState */
  const savedGame = localStorage.getItem('gameState');
  if (savedGame) {
    /* TODO: Load the saved game state */
    /* Hint: Parse the JSON and update gameState */
    gameState = JSON.parse(savedGame);
  }

  /* TODO: Generate shop items */
  /* Hint: Call a function to create available upgrades */
  generateShopItems();

  /* TODO: Start the passive income loop (cookies per second) */
  /* Hint: Use setInterval() to increment cookies over time */
  startPassiveIncome();

  /* TODO: Create a function to update the display */
  /* Hint: Update all DOM elements that show game stats */
  updateDisplay();
};

/* ============================================ */
/* Cookie Click Event Handler */
/* ============================================ */

/* TODO: Add event listener to cookie button */
/* Hint: On click, add cookies to gameState.cookies */
cookieButton.addEventListener('click', function () {
  /* TODO: Add cookiesPerClick to total cookies */
  gameState.cookies += gameState.cookiesPerClick;

  /* TODO: Update the display */
  updateDisplay();

  /* TODO: Add a visual effect when clicked */
  /* Hint: Add animation class to button */
  cookieButton.classList.add('clicked');
  setTimeout(() => {
    cookieButton.classList.remove('clicked');
  }, 100);
});

/* ============================================ */
/* Update Display Function */
/* ============================================ */

function updateDisplay() {
  /* TODO: Update cookie count display */
  cookieCountDisplay.textContent = Math.floor(gameState.cookies);

  /* TODO: Update cookies per second display */
  cpsDisplay.textContent = gameState.cookiesPerSecond.toFixed(1);

  /* TODO: Update cookies per click display */
  cpcDisplay.textContent = gameState.cookiesPerClick;
}
/* TODO: Create a function to generate shop items */
/* Hint: Create upgrade objects with name, cost, effect, etc. */
function generateShopItems() {
    const upgrades = [
        {
            name: 'Cursor',
            cost: 15,
            description: 'Automatically clicks the cookie every second.',
            effect: function() {
                gameState.cookiesPerSecond += 1;
            }
        },
        {
            name: 'Grandma',
            cost: 100,
            description: 'A nice grandma to bake more cookies.',
            effect: function() {
                gameState.cookiesPerSecond += 5;
            }
        },
        {
            name: 'Farm',
            cost: 500,
            description: 'A cookie farm to grow cookies.',
            effect: function() {
                gameState.cookiesPerSecond += 20;
            }
        }
    ];

    upgrades.forEach(upgrade => {
        const shopItem = document.createElement('div');
        

/* TODO: Create a function to generate shop items */
/* Hint: Create upgrade objects with name, cost, effect, etc. */ 
function generateShopItems() {
  /* TODO: Define available upgrades */
  /* Hint: Each upgrade should have: name, cost, description, effect */
  const upgrades = [
    {
      name: 'Cursor',
      cost: 15,
      description: 'Automatically clicks the cookie every second.',
      effect: function () {
        gameState.cookiesPerClick += 1;
      },
    },
    {
      name: 'Grandma',
      cost: 100,
      description: 'A nice grandma to bake more cookies.',
      effect: function () {
        gameState.cookiesPerSecond += 0.5;
      },
    },
    {
      name: 'Farm',
      cost: 500,
      description: 'A cookie farm to grow cookies.',
      effect: function () {
        gameState.cookiesPerSecond += 5;
      },
    },
  ];

  /* TODO: Create HTML elements for each upgrade */
  /* Hint: Loop through upgrades and create shop-item divs */
  upgrades.forEach((upgrade) => {
    const shopItem = document.createElement('div');
    shopItem.className = 'shop-item';
    shopItem.innerHTML = `
      <h3>${upgrade.name}</h3>
      <p>${upgrade.description}</p>
      <p class="item-cost">Cost: ${upgrade.cost} cookies</p>
      <button class="buy-button">Buy</button>
    `;
    shopContainer.appendChild(shopItem);

    /* TODO: Add event listener to buy button */
    /* Hint: Check if player has enough cookies, deduct cost, apply effect */
    const buyButton = shopItem.querySelector('.buy-button');
    buyButton.addEventListener('click', function () {
      buyUpgrade(upgrade);
    });
  });
}

/* ============================================ */
/* Buy Upgrade Function */
/* ============================================ */

/* TODO: Create a function to buy upgrades */
/* Hint: Check if player has enough cookies, deduct and apply effect */
function buyUpgrade(upgrade) {
  /* TODO: Check if player has enough cookies */
  if (gameState.cookies >= upgrade.cost) {
    /* TODO: Deduct cost from cookies */
    gameState.cookies -= upgrade.cost;

    /* TODO: Apply the upgrade effect */
    upgrade.effect();

    /* TODO: Add upgrade to purchased list (optional) */
    gameState.upgrades.push(upgrade.name);

    /* TODO: Update display */
    updateDisplay();

    /* TODO: Add visual feedback */
    console.log('Upgrade purchased:', upgrade.name);
  } else {
    /* TODO: Show notification that player doesn't have enough cookies */
    alert('Not enough cookies to purchase this upgrade!');
  }
}

/* ============================================ */
/* Passive Income Function */
/* ============================================ */

/* TODO: Create a function for passive income (cookies per second) */
/* Hint: Use setInterval to increment cookies every second */
function startPassiveIncome() {
  /* TODO: Add cookiesPerSecond to total cookies */
  setInterval(() => {
    gameState.cookies += gameState.cookiesPerSecond;
    updateDisplay();
  }, 1000); // Every 1000ms (1 second)
}

/* ============================================ */
/* Save and Load Game Functions */
/* ============================================ */

/* TODO: Add event listener to save button */
/* Hint: Save gameState to localStorage */
saveButton.addEventListener('click', function () {
  /* TODO: Save current game state to localStorage */
  /* Hint: Use JSON.stringify() to convert object to string */
  localStorage.setItem('gameState', JSON.stringify(gameState));

  /* TODO: Show confirmation message */
  alert('Game saved successfully!');
  console.log('Game saved:', gameState);
});

/* TODO: Add event listener to load button */
/* Hint: Load gameState from localStorage */
loadButton.addEventListener('click', function () {
  /* TODO: Load saved game state from localStorage */
  const savedGame = localStorage.getItem('gameState');

  if (savedGame) {
    /* TODO: Parse and apply the saved state */
    gameState = JSON.parse(savedGame);

    /* TODO: Update display */
    updateDisplay();

    /* TODO: Show confirmation message */
    alert('Game loaded successfully!');
  } else {
    /* TODO: Show message if no save exists */
    alert('No saved game found!');
  }
});

/* ============================================ */
/* Back Button Function */
/* ============================================ */

/* TODO: Add event listener to back button */
/* Hint: Navigate back to home page */
backButton.addEventListener('click', function () {
  /* TODO: Confirm before leaving */
  /* Hint: Ask if user wants to save before leaving */
  const confirmed = confirm(
    'Would you like to save your game before leaving?'
  );

  if (confirmed) {
    /* TODO: Save the game */
    localStorage.setItem('gameState', JSON.stringify(gameState));
    alert('Game saved!');
  }

  /* TODO: Redirect to home page */
  window.location.href = 'home.html';
});

/* ============================================ */
/* Extra Features (Optional) */
/* ============================================ */

/* TODO: Implement auto-save feature */
/* Hint: Use setInterval to save game state periodically */
setInterval(() => {
  localStorage.setItem('gameState', JSON.stringify(gameState));
}, 30000); // Auto-save every 30 seconds

/* TODO: Add keyboard shortcuts */
/* Hint: Listen for keyboard events and trigger actions */
document.addEventListener('keydown', function (event) {
  if (event.key === 's' || event.key === 'S') {
    // Press 'S' to save
    localStorage.setItem('gameState', JSON.stringify(gameState));
    console.log('Game auto-saved via keyboard!');
  }
});

/* TODO: Add more game features */
/* Hint: Achievements, multipliers, special events, etc. */
// Add more features here as needed