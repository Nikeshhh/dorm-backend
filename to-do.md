## Добавить удобства для работы
- [X] Сделать доку
- [X] Сделать шорткаты команд через makefile
- [X] Задокументировать весь API
## Избавиться от логики во views
Сделать все через сервисы, чтобы избваиться от вью логики.
Аутентификация остается на месте. В первую очередь сделать и посмотреть доку.
### Дежурства
Логики в сериализаторах нет.
- [ ] Избавиться от get_queryset логики
- [ ] Сделать сервис для DutyRecords
- [ ] Сделать сервис для обмена
- [ ] Сделать сервис для замены

### Журнал прачечной
- [ ] Убрать get_is_owned из сериализатора
- [ ] Сделать сервис для журнала

### Журнал комнаты
- [ ] Убрать логику создания из сериализатора
- [ ] 