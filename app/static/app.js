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
});