-- Запрос 1. Получение списка всех мероприятий с сортировкой по дате
SELECT
    id,
    title,
    date,
    max_seats,
    registered
FROM events
ORDER BY date;

-- Запрос 2. Поиск мероприятий по вместимости
SELECT
    id,
    title,
    date,
    max_seats,
    registered
FROM events
WHERE max_seats >= 50
ORDER BY max_seats DESC;

-- Запрос 3. Получение списка всех участников
SELECT
    id,
    name,
    email
FROM participants
ORDER BY name;

-- Запрос 4. Поиск участников с почтой на gmail
SELECT
    id,
    name,
    email
FROM participants
WHERE email LIKE '%@gmail.com';

-- Запрос 5. Оплаченные билеты
SELECT
    id,
    event_id,
    participant_id,
    status,
    number 
FROM tickets
WHERE status = 'оплачен'
ORDER BY number;

-- Запрос 6. Полная информация о билете
SELECT
    tickets.id,
    tickets.number AS ticket_number,
    tickets.status AS ticket_status,
    events.title AS event_title,
    events.date AS event_date,
    events.max_seats AS event_max_seats,
    events.registered AS event_registered,
    participants.name AS participant_name,
    participants.email
FROM tickets
JOIN events
ON tickets.event_id = events.id
JOIN participants
ON tickets.participant_id = participants.id;

-- Запрос 7. Список всех билетов с именами участников
SELECT
    tickets.number AS ticket_number,
    tickets.status,
    participants.name AS participant_name
FROM tickets
JOIN participants ON tickets.participant_id = participants.id
ORDER BY participants.name;

-- Запрос 8. Общее количество билетов
SELECT COUNT(*) AS tickets_count
FROM tickets
WHERE status != 'отменён';

-- Запрос 9. Количество билетов по мероприятиям
SELECT
    events.title AS events_title,
    COUNT(tickets.id) AS tickets_count
FROM events
LEFT JOIN tickets
ON events.id = tickets.event_id
AND status != 'отменён'
GROUP BY events.id, events.title
ORDER BY tickets_count DESC;

-- Запрос 10. Мероприятия с количеством билетов больше заданного
SELECT
    events.title AS events_title,
    COUNT(tickets.id) AS tickets_count
FROM events
JOIN tickets
ON events.id = tickets.event_id
WHERE tickets.status != 'отменён'
GROUP BY events.id, events.title
HAVING COUNT(tickets.id) >= 1
ORDER BY tickets_count DESC;