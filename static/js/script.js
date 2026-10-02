// Confirm before running grading, since it deletes previous results for that question
document.addEventListener("DOMContentLoaded", function () {
    const gradeForm = document.querySelector('form[action*="grade_answers"]');
    if (gradeForm) {
        gradeForm.addEventListener("submit", function (event) {
            const confirmed = confirm(
                "Running grading will delete any previous results for this question. Continue?"
            );
            if (!confirmed) {
                event.preventDefault();
            }
        });
    }

    // Auto-hide flash messages after 4 seconds
    const flashes = document.querySelectorAll(".flashes li");
    flashes.forEach(function (flash) {
        setTimeout(function () {
            flash.style.transition = "opacity 0.5s ease";
            flash.style.opacity = "0";
            setTimeout(function () {
                flash.remove();
            }, 500);
        }, 4000);
    });
});