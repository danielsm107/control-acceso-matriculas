const lottieAnimations = {};

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".lottie-player").forEach(player => {
    const id = player.id;
    const path = player.dataset.path;
    lottieAnimations[id] = lottie.loadAnimation({
      container: player,
      renderer: 'svg',
      loop: false,
      autoplay: false,
      path: path
    });
  });
});

function playLottie(button) {
  const container = button.querySelector(".lottie-container");
  const svgIcon = container.querySelector(".lottie-icon");
  const player = container.querySelector(".lottie-player");
  const anim = lottieAnimations[player.id];

  svgIcon.style.display = "none";
  player.style.display = "block";

  if (anim) {
    anim.goToAndPlay(0, true);
    setTimeout(() => {
      button.closest("form").submit();
    }, 800);
  }
}
