const API_URL = "https://gostnodeapi.onrender.com/signup";

const form = document.getElementById("signupForm");
const emailEl = document.getElementById("emailInput");
const msgEl = document.getElementById("signupMsg");

if (!form || !emailEl || !msgEl) {
  console.warn("Signup elements not found:", { form, emailEl, msgEl });
} else {
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    msgEl.textContent = "Submitting...";
    const email = emailEl.value.trim();

    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });

      const data = await res.json().catch(() => ({}));

      if (res.ok) {
        msgEl.textContent = "You're in. Welcome to The Network.";
        form.reset();
      } else {
        // FastAPI often returns { detail: ... } on errors
        msgEl.textContent =
          data?.detail?.[0]?.msg || data?.detail || "Something went wrong.";
      }
    } catch (err) {
      console.error(err);
      msgEl.textContent = "Network error. Please try again.";
    }
  });
}
const player = document.getElementById("player");
const playStopBtn = document.getElementById("playStop");
const volume = document.getElementById("volume");

if (player && playStopBtn) {
  playStopBtn.addEventListener("click", async () => {
    if (player.paused) {
      await player.play();
      playStopBtn.textContent = "Stop";
    } else {
      player.pause();
      player.currentTime = 0;
      playStopBtn.textContent = "Play";
    }
  });

  player.addEventListener("ended", () => {
    playStopBtn.textContent = "Play";
    player.currentTime = 0;
  });
}

if (player && volume) {
  volume.addEventListener("input", () => {
    player.volume = Number(volume.value);
  });
}
