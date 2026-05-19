const container = document.getElementById("projects");
const search = document.getElementById("search");
const categoryFilter =
    document.getElementById("categoryFilter");

const themeToggle =
    document.getElementById("themeToggle");

let allProjects = [];

fetch("./projects.json")
    .then(r => r.json())
    .then(projects => {

        allProjects = projects;

        setupCategories(projects);

        render(projects);
    });

function setupCategories(projects) {

    const categories =
        [...new Set(projects.map(p => p.category))];

    categories.forEach(cat => {

        const option =
            document.createElement("option");

        option.value = cat;

        option.textContent = cat;

        categoryFilter.appendChild(option);
    });
}

function render(projects) {

    container.innerHTML = "";

    projects.forEach(project => {

        const a = document.createElement("a");

        a.href = project.path;

        a.innerHTML = `
      <div class="card">

        ${project.thumbnail
                ? `<img src="${project.thumbnail}" />`
                : ""
            }

        <div class="content">

          <div class="title">
            ${project.name}
          </div>

          <div class="description">
            ${project.description || ""}
          </div>

          <div class="meta">

            <span class="tag">
              ${project.category}
            </span>

            ${project.tags.map(tag => `
              <span class="tag">${tag}</span>
            `).join("")}

          </div>

          <div class="date">
            Updated: ${project.lastUpdated}
          </div>

        </div>
      </div>
    `;

        container.appendChild(a);
    });
}

function filterProjects() {

    const text =
        search.value.toLowerCase();

    const category =
        categoryFilter.value;

    const filtered = allProjects.filter(project => {

        const matchesText =
            project.name.toLowerCase().includes(text)
            ||
            project.description
                .toLowerCase()
                .includes(text)
            ||
            project.tags.join(" ")
                .includes(text);

        const matchesCategory =
            category === "all"
            ||
            project.category === category;

        return matchesText && matchesCategory;
    });

    render(filtered);
}

search.addEventListener(
    "input",
    filterProjects
);

categoryFilter.addEventListener(
    "change",
    filterProjects
);

themeToggle.addEventListener(
    "click",
    () => {

        document.body.classList.toggle("dark");

        localStorage.setItem(
            "theme",
            document.body.classList.contains("dark")
                ? "dark"
                : "light"
        );
    }
);

if (localStorage.getItem("theme") === "dark") {
    document.body.classList.add("dark");
}