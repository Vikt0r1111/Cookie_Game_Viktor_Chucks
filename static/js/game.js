const cookieEl = document.getElementById("cookie");
const cookieCountEl = document.getElementById("cookie-count");
const upgradesEl = document.getElementById("upgrades");
const shopEl = document.getElementById("shop");
const levelupShopEl = document.getElementById("levelup-shop");
const cookieContainer = document.getElementById("cookie-container");

let userData = null;
const maxFallingCookies = 15;
let currentFallingCount = 0;

const upgradeOrder = ["doubleClick", "grandma", "farm", "factory", "mine", "bank", "temple", "wizardTower", "shipment"];

document.getElementById('popup-logout-btn').addEventListener('click', async () => {
  const response = await fetch('/logout', { method: 'POST' });

    window.location.href = '/login';
  });

function spawnFallingCookie() {
    if (currentFallingCount >= maxFallingCookies) return;

    const fCookie = document.createElement("div");
    fCookie.className = "falling-cookie";
    
    const rect = cookieContainer.getBoundingClientRect();
    const randomX = Math.random() * (rect.width - 40);
    fCookie.style.left = randomX + "px";

    const duration = 1.5 + Math.random() * 1.5;
    fCookie.style.animationDuration = duration + "s";

    cookieContainer.appendChild(fCookie);
    currentFallingCount++;

    fCookie.addEventListener("animationend", () => {
        fCookie.remove();
        currentFallingCount--;
    });
}

async function loadGame() {
    const res = await fetch("/cookie_game", { method: "POST" });
    userData = await res.json();
    if(userData.username) document.getElementById("popup-username").textContent = userData.username;
    render();
}

function render() {
    const totalCps = Math.round(userData.cookiesPerSecond || 0);
    cookieCountEl.textContent = `${Math.round(userData.cookies)} cookies (${totalCps} CPS)`;

    upgradesEl.innerHTML = "";
    upgradeOrder.forEach(name => {
        const up = userData.upgrades[name];
        if (up.quantity > 0) {
            let cpsText = name !== "doubleClick" ? `<br>CPS: ${Math.round(up.cookiesPerSecond * up.level)}` : "";
            upgradesEl.innerHTML += `<div class="upgrade"><b>${name}</b><br>Qty: ${up.quantity}<br>Lvl: ${up.level}${cpsText}</div>`;
        }
    });

    levelupShopEl.innerHTML = "";
    upgradeOrder.forEach(name => {
        const up = userData.upgrades[name];
        if (up.quantity > 0) {
            levelupShopEl.innerHTML += `
                <div class="levelup-item">
                    <b>${name}</b> (Lvl ${up.level})<br>
                    Price: ${Math.round(up.levelup_price || up.price)}
                    <button onclick="buyLevelUp('${name}')">Level Up</button>
                </div>`;
        }
    });

    shopEl.innerHTML = "";
    for (let i = 0; i < upgradeOrder.length; i++) {
        const name = upgradeOrder[i];
        const up = userData.upgrades[name];
        if (i > 0 && userData.upgrades[upgradeOrder[i - 1]].quantity === 0) break;
        
        shopEl.innerHTML += `
            <div class="shop-item">
                <b>${name}</b><br> Price: ${Math.round(up.price)}
                <button onclick="buyUpgrade('${name}')">Buy</button>
            </div>`;
    }
}

cookieEl.addEventListener("click", async () => {
    spawnFallingCookie();
    await fetch("/click", { method: "POST" });
    await loadGame();
});

async function buyUpgrade(name) {
    const form = new FormData();
    form.append("upgrade_name", name);
    await fetch("/buy_upgrades", { method: "POST", body: form });
    await loadGame();
}

async function buyLevelUp(name) {
    const form = new FormData();
    form.append("upgrade_name", name);
    await fetch("/buy_levelup", { method: "POST", body: form });
    await loadGame();
}

setInterval(async () => {
    await fetch("/upgrade_click", { method: "POST" });
    await loadGame();
    
    if (userData && userData.cookiesPerSecond > 0) {
        const cps = userData.cookiesPerSecond;

        let amountToSpawn = Math.min(Math.ceil(cps / 10), 5); 

        for (let i = 0; i < amountToSpawn; i++) {
            const delay = Math.random() * 800;
            setTimeout(() => {
                spawnFallingCookie();
            }, delay);
        }
    }
}, 1000);

const accountIcon = document.getElementById("account-icon");
const accountPopup = document.getElementById("account-popup");
accountIcon.onclick = () => accountPopup.style.display = accountPopup.style.display === "block" ? "none" : "block";

document.addEventListener("DOMContentLoaded", loadGame);
