// =========================
// Flood Prediction System
// =========================

document.addEventListener("DOMContentLoaded", function () {

    console.log("Flood Prediction System Loaded");

    // Smooth button animation
    const buttons = document.querySelectorAll("button, .btn");

    buttons.forEach(button => {

        button.addEventListener("mouseenter", function () {

            button.style.transform = "scale(1.05)";

        });

        button.addEventListener("mouseleave", function () {

            button.style.transform = "scale(1)";

        });

    });

});