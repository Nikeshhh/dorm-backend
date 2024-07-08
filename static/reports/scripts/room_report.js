// Получаем элементы
let room_record_modal = document.getElementById("room_record_modal");
let room_record_btn = document.getElementById("open_room_record_modal");
let span = document.getElementById("room_record_close");

// Открываем модальное окно при нажатии на кнопку
room_record_btn.onclick = function() {
    room_record_modal.style.display = "block";
}

// Закрываем модальное окно при нажатии на крестик
span.onclick = function() {
    room_record_modal.style.display = "none";
}