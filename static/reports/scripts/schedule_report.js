// Получаем элементы
let duty_schedule_modal = document.getElementById("duty_schedule_modal");
let duty_schedule_btn = document.getElementById("open_duty_schedule_modal");
let duty_schedule_span = document.getElementById("duty_schedule_close");

// Открываем модальное окно при нажатии на кнопку
duty_schedule_btn.onclick = function() {
    duty_schedule_modal.style.display = "block";
}

// Закрываем модальное окно при нажатии на крестик
duty_schedule_span.onclick = function() {
    duty_schedule_modal.style.display = "none";
}