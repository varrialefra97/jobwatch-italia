let allJobs = [];

const jobsEl = document.getElementById("jobs");
const emptyEl = document.getElementById("empty");
const totalJobsEl = document.getElementById("totalJobs");
const lastUpdatedEl = document.getElementById("lastUpdated");
const searchInput = document.getElementById("searchInput");
const categoryFilter = document.getElementById("categoryFilter");
const sourceFilter = document.getElementById("sourceFilter");
const resetBtn = document.getElementById("resetBtn");

async function loadJobs() {
  try {
    const response = await fetch("data/jobs.json?t=" + Date.now());
    const data = await response.json();

    allJobs = data.jobs || [];

    totalJobsEl.textContent = allJobs.length;
    lastUpdatedEl.textContent = data.updated_at
      ? "Aggiornamento: " + new Date(data.updated_at).toLocaleString("it-IT")
      : "Aggiornamento: —";

    populateCompanies();
    renderJobs();
  } catch (error) {
    console.error("Errore caricamento jobs.json:", error);
    allJobs = [];
    renderJobs();
  }
}

function populateCompanies() {
  const companies = [...new Set(allJobs.map(job => job.company).filter(Boolean))].sort();

  sourceFilter.innerHTML = '<option value="all">Tutte le aziende</option>';

  companies.forEach(company => {
    const option = document.createElement("option");
    option.value = company;
    option.textContent = company;
    sourceFilter.appendChild(option);
  });
}

function renderJobs() {
  const search = searchInput.value.toLowerCase().trim();
  const category = categoryFilter.value;
  const source = sourceFilter.value;

  const filtered = allJobs.filter(job => {
    const text = [
      job.title,
      job.company,
      job.location,
      job.degree,
      job.category
    ].join(" ").toLowerCase();

    const matchesSearch = !search || text.includes(search);
    const matchesSource = source === "all" || job.company === source;

    let matchesCategory = true;

    if (category === "marketing") {
      matchesCategory =
        (job.category || "").toLowerCase().includes("marketing") ||
        (job.category || "").toLowerCase().includes("comunicazione") ||
        (job.title || "").toLowerCase().includes("marketing") ||
        (job.title || "").toLowerCase().includes("communication") ||
        (job.title || "").toLowerCase().includes("comunicazione");
    }

    if (category === "triennale") {
      matchesCategory =
        (job.degree || "").toLowerCase().includes("triennale") ||
        text.includes("laurea triennale") ||
        text.includes("bachelor");
    }

    return matchesSearch && matchesSource && matchesCategory;
  });

  jobsEl.innerHTML = "";

  totalJobsEl.textContent = filtered.length;
  emptyEl.hidden = filtered.length > 0;

  filtered.forEach(job => {
    const article = document.createElement("article");
    article.className = "job-card";

    article.innerHTML = `
      <div>
        <h2>${escapeHtml(job.title || "Ruolo non specificato")}</h2>
        <p><strong>${escapeHtml(job.company || "Azienda non specificata")}</strong></p>
        <p>${escapeHtml(job.location || "Località non specificata")}</p>
        <p>${escapeHtml(job.degree || "")}</p>
        <span>${escapeHtml(job.category || "")}</span>
      </div>
      <a href="${escapeHtml(job.url || "#")}" target="_blank" rel="noopener noreferrer">
        Candidati sul sito ufficiale
      </a>
    `;

    jobsEl.appendChild(article);
  });
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

searchInput.addEventListener("input", renderJobs);
categoryFilter.addEventListener("change", renderJobs);
sourceFilter.addEventListener("change", renderJobs);

resetBtn.addEventListener("click", () => {
  searchInput.value = "";
  categoryFilter.value = "all";
  sourceFilter.value = "all";
  renderJobs();
});

loadJobs();
