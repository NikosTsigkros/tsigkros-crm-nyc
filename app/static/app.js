const button = document.getElementById("ping");
const result = document.getElementById("result");

if (button && result) {
  button.addEventListener("click", async () => {
    try {
      const response = await fetch("/ping");
      const data = await response.json();
      result.textContent = data.message;
    } catch (error) {
      result.textContent = "Ping failed.";
    }
  });
}
