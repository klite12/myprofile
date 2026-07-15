document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("contact-form");
  const status = document.getElementById("form-status");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    status.textContent = "Sending...";
    status.classList.remove("error");

    const payload = {
      name: form.name.value,
      email: form.email.value,
      message: form.message.value,
    };

    try {
      const res = await fetch("/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await res.json();

      if (data.ok) {
        status.textContent = data.message;
        form.reset();
      } else {
        status.textContent = data.error || "Something went wrong. Please try again.";
        status.classList.add("error");
      }
    } catch (err) {
      status.textContent = "Couldn't reach the server. Please try again.";
      status.classList.add("error");
    }
  });
});
