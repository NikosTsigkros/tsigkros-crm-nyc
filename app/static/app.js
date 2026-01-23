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
});