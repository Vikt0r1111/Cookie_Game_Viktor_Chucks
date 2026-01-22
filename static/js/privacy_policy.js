const translations = {
    en: { 
        terms: privacy_policy_terms_en,
        title: "Privacy Policy"
    },
    es: { 
        terms: Politica_de_Privacidad_es,
        title: "Política de Privacidad" 
    },  
    fr: { 
        terms: Politique_de_Confidentialite_fr, 
        title: "Politique de Confidentialité" 
    },
    de: { 
        terms: Datenschutz_Bestimmungen_de, 
        title: "Datenschutz-Bestimmungen"
    },
    it: { 
        terms: Politica_sulla_Privacy_it, 
        title: "Politica sulla Privacy" 
    }
};

let currentLanguage = "en"; // Default language

function updatePrivacyPolicy() {
    const policyContainer = document.getElementById("privacy-policy-content");
    const titleElement = document.getElementById("privacy-policy-title");

    policyContainer.innerHTML = translations[currentLanguage].terms;
    titleElement.textContent = translations[currentLanguage].title;
}

document.querySelectorAll(".language-select").forEach(button => {
    button.addEventListener("click", () => {
        currentLanguage = button.getAttribute("data-lang");
        updatePrivacyPolicy();

        // Update active button styling
        document.querySelectorAll(".language-select").forEach(b => b.classList.remove("active"));
        button.classList.add("active");
    });
});

// Initial load
updatePrivacyPolicy();
document.querySelector(`.language-select[data-lang="${currentLanguage}"]`).classList.add("active");

