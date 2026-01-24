const button = document.getElementById("ping");
const result = document.getElementById("result");

if (button && result) {
  button.addEventListener("click", async () => {
    try {
      const response = await fetch("/api/ping");
      const data = await response.json();
      result.textContent = data.message;
    } catch (error) {
      result.textContent = "Ping failed.";
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  const employeeStats = document.querySelector("[data-employee-stats]");
  if (employeeStats) {
    fetch("/api/employee/stats")
      .then((res) => res.json())
      .then((data) => {
        employeeStats.querySelectorAll("[data-stat]").forEach((node) => {
          const key = node.getAttribute("data-stat");
          node.textContent = data[key] ?? 0;
        });
      })
      .catch(() => {
        employeeStats.querySelectorAll("[data-stat]").forEach((node) => {
          node.textContent = "-";
        });
      });
  }

  const managerFilters = document.querySelector("[data-manager-filters]");
  if (managerFilters) {
    const loadManagerStats = () => {
      const days = managerFilters.querySelector("[name='days']").value;
      const noResponseN = managerFilters.querySelector("[name='noResponseN']").value;
      fetch(`/api/manager/stats?days=${days}&no_response_n=${noResponseN}`)
        .then((res) => res.json())
        .then((data) => {
          renderManagerTable("[data-manager-contacts] tbody", data.contactsPerEmployee, 2, (row) => [
            row.employee,
            row.count,
          ]);
          renderManagerTable("[data-manager-inactive] tbody", data.inactiveCustomers, 2, (row) => [
            row.name,
            row.lastContact,
          ]);
          renderManagerTable("[data-manager-noresponse] tbody", data.noResponseCustomers, 1, (row) => [
            row.name,
          ]);
          renderCategoryPills("[data-manager-categories]", data.categoryCounts);
        })
        .catch(() => {
          renderManagerTable("[data-manager-contacts] tbody", [], 2, () => []);
        });
    };

    managerFilters.addEventListener("submit", (event) => {
      event.preventDefault();
      loadManagerStats();
    });

    loadManagerStats();
  }

  const tableFilter = document.querySelector("[data-table-filter]");
  if (tableFilter) {
    const table = document.querySelector("[data-filter-table]");
    tableFilter.addEventListener("input", () => {
      const term = tableFilter.value.toLowerCase();
      table.querySelectorAll("tbody tr").forEach((row) => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(term) ? "" : "none";
      });
    });
  }
});

function renderManagerTable(selector, rows, columnCount, mapper) {
  const tbody = document.querySelector(selector);
  if (!tbody) return;
  tbody.innerHTML = "";
  if (!rows || rows.length === 0) {
    const emptyRow = document.createElement("tr");
    const cell = document.createElement("td");
    cell.colSpan = columnCount;
    cell.textContent = "No data available";
    emptyRow.appendChild(cell);
    tbody.appendChild(emptyRow);
    return;
  }
  rows.forEach((row) => {
    const tr = document.createElement("tr");
    mapper(row).forEach((value) => {
      const td = document.createElement("td");
      td.textContent = value;
      tr.appendChild(td);
    });
    tbody.appendChild(tr);
  });
}

function renderCategoryPills(selector, data) {
  const container = document.querySelector(selector);
  if (!container) return;
  container.innerHTML = "";
  const entries = Object.entries(data || {});
  if (entries.length === 0) {
    const pill = document.createElement("span");
    pill.className = "pill";
    pill.textContent = "No new customers";
    container.appendChild(pill);
    return;
  }
  entries.forEach(([category, count]) => {
    const pill = document.createElement("span");
    pill.className = "pill";
    pill.textContent = `${category}: ${count}`;
    container.appendChild(pill);
  });
}
