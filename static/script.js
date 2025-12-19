const API_URL = "http://127.0.0.1:8000/signup";
// later: https://your-api.onrender.com/signup

const form = document.getElementById("signup-form");

if (!form) {
  console.warn("signup-form not found on page yet");
} else {
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const emailEl = document.getElementById("email");
    const websiteEl = document.getElementById("website");

    const email = emailEl ? emailEl.value : "";
    const website = websiteEl ? websiteEl.value : "";

    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, website }),
      });

      if (res.ok) {
        alert("You're in. Welcome to The Network.");
        form.reset();
      } else {
        alert("Something went wrong.");
      }
    } catch (err) {
      console.error(err);
      alert("Network error. Is the API running?");
    }
  });
}
