## Auth
Приложение для аутентификации пользователей.

- POST /api/v1/auth/log_in/ -> /api/v1/auth/login/ - Вход через юзернейм и пароль
- POST /api/v1/auth/logout/ - Выход
- GET /api/v1/auth/is_authenticated/ -> /api/v1/auth/is-authenticated/ - Проверка пользователя на аутентифицированность

## Duties
Приложения для работы с дежурствами и их обменом.

### DutyRecords
- GET /api/v1/duties/records/ - Список всех дежурств
- GET /api/v1/duties/records/{duty_id}/duties_to_swap/ -> /api/v1/duties/records/{duty_id}/to-swap/ - Получить список дежурств, доступных для обмена с выбранным дежурством (duty_id)
- GET /api/v1/duties/records/my_duties/ -> /api/v1/duties/records/my/ - Получить список дежурств пользователя
- GET /api/v1/duties/records/nearest_duty/ -> /api/v1/duties/records/nearest/ - Получить ближайшее дежурство пользователя

### SwapDuties
- GET /api/v1/duties/swap-duties/ - Получить список всех запросов на обмен дежурствами.
- POST /api/v1/duties/swap-duites/{request_id}/accept_swap_duites_request/ -> /api/v1/duties/swap-duites/{request_id}/accept/ - Принять запрос на обмен дежурствами с переданным {request_id}
- POST /api/v1/duties/swap-duites/{request_id}/cancel_swap_duites_request/ -> /api/v1/duties/swap-duites/{request_id}/cancel/ - Отменить запрос на обмен дежурствами с переданным {request_id}
- POST /api/v1/duties/swap-duites/{request_id}/decline_swap_duites_request/ -> /api/v1/duties/swap-duites/{request_id}/decline/ - Отклонить запрос на обмен дежурствами с переданным {request_id}
- POST /api/v1/duties/swap-duites/create_swap_duites_request/ -> /api/v1/duties/swap-duites/ - Создать запрос на обмен дежурствами
- GET /api/v1/duties/swap-duites/get_incoming_requests/ -> /api/v1/duties/swap-duites/incoming/ - Получить список входящих запросов на обмен для текущего пользователя

### SwapPeople
- GET /api/v1/swap-people/ - Получить список всех запросов на замену
- POST /api/v1/duties/swap-people/{request_id}/accept_swap_people_request/ -> /api/v1/duties/swap-people/{request_id}/accept/ - Принять запрос на замену с переданным {request_id}
- POST /api/v1/duties/swap-people/{request_id}/cancel_swap_people_request/ -> /api/v1/duties/swap-people/{request_id}/cancel/ - Отменить запрос на замену с переданным {request_id}
- POST /api/v1/duties/swap-people/{request_id}/decline_swap_people_request/ -> /api/v1/duties/swap-people/{request_id}/decline/ - Отклонить запрос на замену с переданным {request_id}
- POST /api/v1/duties/swap-people/create_swap_people_request/ -> /api/v1/duties/swap-people/ - Создать запрос на замену
- GET /api/v1/duties/swap-people/get_incoming_requests/ -> /api/v1/duties/swap-people/incoming/ - Получить список входящих запросов на замену для текущего пользователя

### SwapRequests
- GET /api/v1/duties/swap-requests/ - Получить список всех (?) запросов на замену и обмен

### Laundry
- GET /api/v1/laundry/records/ - Получить список всех записей
- POST /api/v1/laundry/records/{record_id}/free_record/ -> /api/v1/laundry/records/{record_id}/free/ - Освободить выбранную запись
- POST /api/v1/laundry/records/{record_id}/take_record/ -> /api/v1/laundry/records/{record_id}/take/ - Занять выбранную запись
- GET /api/v1/laundry/records/my_records_today/ -> /api/v1/laundry/records/today/my/ - Получить список занятых сегодня записей текущим пользователем
- GET /api/v1/laundry/records/today_records_list/ -> /api/v1/laundry/records/today/ - Получить список записей на сегодня
- GET /api/v1/laundry/records/today_records_stats/ -> /api/v1/laundry/records/today/stats/ - Получить статистику о количестве оставшихся записей на сегодня

## Proposals
Приложения для управления заявками.

### RepairProposals
- GET /api/v1/proposals/repair/ - Получить список всех заявок на ремонт
- POST /api/v1/proposals/repair/ - Создать заявку на ремонт
- POST /api/v1/proposals/repair/{proposal_id}/accept/ - Принять заявку на ремонт к исполнению
- POST /api/v1/proposals/repair/{proposal_id}/cancel/ - Отменить заявку на ремонт
- POST /api/v1/proposals/repair/{proposal_id}/close/ - Закрыть заявку на ремонт
- POST /api/v1/proposals/repair/{proposal_id}/decline/ - Отказаться от исполнения заявки на ремонт
- GET /api/v1/proposals/repair/my_proposals/ -> /api/v1/proposals/repair/my/ - Получить список заявок, созданных пользователем

## Rooms
Приложения для управления книгой комнаты

- GET /api/v1/rooms/create_room_records/ -> /api/v1/rooms/ - Получить список комнат
- POST /api/v1/rooms/create_room_records/ -> /api/v1/rooms/records/ - Создать запись в книге комнаты
- PUT /api/v1/rooms/create_room_records/{record_id} -> /api/v1/rooms/records/{record_id} - Редактировать запись в книге комнаты
- PATCH /api/v1/rooms/create_room_records/{record_id} -> /api/v1/rooms/records/{record_id} - Редактировать запись в книге комнаты
- GET /api/v1/rooms/create_room_records/today_created/ -> /api/v1/rooms/records/today/created/ - Получить список записей, созданных сегодня (текущим пользователем?)
- GET /api/v1/rooms/room_records/ -> /api/v1/rooms/records/ - Получить список всех записей комнаты пользователя
- GET /api/v1/rooms/room_records/{record_id} -> /api/v1/rooms/records/{record_id}/ - Получить подробную информацию о записе в книге комнаты пользователя
- GET /api/v1/rooms/room_records/my_last_room_record/ -> /api/v1/rooms/records/last/ - Получить подробную информацию о последней записи в книге комнаты пользователя

## Users

- GET /api/v1/users/users-views/list_residents/ -> /api/v1/users/residents/ - Получить список всех проживающих
- GET /api/v1/users/users-views/me/ -> /api/v1/users/me/ - Получить информацию о текущем пользователе

### Что зарефакторить
- Убрать андерскоры
- Слишком длинные префиксы
- Некоторые запросы объединить под один префикс