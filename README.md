# Сервис регистрации участников конференции

Учебное веб-приложение на Django для управления участниками конференции,
мероприятиями и билетами.

## 1. Назначение проекта

Сервис регистрации участников конференции — учебное приложение, которое
позволяет хранить сведения об участниках, мероприятиях и билетах,
выполнять основные операции с этими объектами и предоставлять доступ
к информации через веб-интерфейс на Django.

Проект развивается поэтапно: консольная версия приложения (ПР1–ПР3)
дополнена веб-интерфейсом (ПР5), переведена на систему шаблонов Django (ПР6),
получила слой реляционного хранения данных SQLite (ПР7) и переведена
на Django ORM (ПР9).

## 2. Используемые технологии

- Python 3;
- Django 5.2;
- Django ORM;
- Django Template Language (DTL);
- HTML5;
- CSS3;
- JavaScript;
- Bootstrap 5.3;
- SQLite;
- JSON;
- Git;
- pytest;
- flake8.

## 3. Предметная область

В системе используются три основные сущности:

- **Участник (Participant)** — идентификатор, имя, email;
- **Мероприятие (Event)** — идентификатор, название, дата, максимальное
  количество мест, количество зарегистрированных;
- **Билет (Ticket)** — идентификатор, ссылка на мероприятие, ссылка
  на участника, статус (`забронирован`, `оплачен`, `отменён`), номер билета.

Для предметной области реализованы собственные Python-классы
`Participant`, `Event` и `Ticket` (пакет `models/`), а также Django-модели
в приложениях `participants` и `events`.

### 3.1. Django-модели (ПР9)

- `Participant` (`participants/models.py`): `name`, `email`.
- `Event` (`events/models.py`): `title`, `date`, `max_seats`, `registered`.
- `Ticket` (`events/models.py`): `event` (FK → `Event`), `participant`
  (FK → `Participant`), `status`, `number`.

Связи: `Ticket.event` → `Event`, `Ticket.participant` → `Participant`
(ForeignKey, `on_delete=CASCADE`, `related_name='tickets'`).

### 3.2. Исходная база данных (ПР7)

На этапе ПР7 данные были перенесены из JSON-файлов в базу данных SQLite
(`data/conference.sqlite`). Эта база сохранена как источник исходных данных
и не используется представлениями после перехода на ORM.

## 4. Структура проекта

```
conference-registration-service/
│
├── README.md
├── requirements.txt
├── manage.py
├── db.sqlite3 
├── main.py
├── storage.py
├── utils.py
│
├── conference/                # Django-проект
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── templates/                 # шаблоны уровня проекта
│   ├── base.html
│   └── includes/
│       └── navigation.html
│
├── homepage/                  # приложение: главная страница
│   ├── static/
│   │   └── homepage/
│   │       ├── css/
│   │       │   └── style.css
│   │       ├── js/
│   │       │   └── main.js
│   │       └── img/
│   │           └── logo.webp
│   ├── templates/
│   │   └── homepage/
│   │       └── index.html
│   ├── urls.py
│   └── views.py
│
├── participants/              # приложение: участники
│   ├── migrations/            # миграции (ПР9)
│   ├── models.py              # модель Participant (ПР9)
│   ├── templates/
│   │   └── participants/
│   │       ├── participant_list.html
│   │       ├── participant_detail.html
│   │       └── includes/
│   │           └── participant_card.html
│   ├── urls.py
│   └── views.py
│
├── events/                    # приложение: мероприятия и билеты
│   ├── migrations/            # миграции (ПР9)
│   ├── models.py              # модели Event, Ticket (ПР9)
│   ├── templates/
│   │   └── events/
│   │       ├── event_list.html
│   │       ├── event_detail.html
│   │       ├── tickets.html
│   │       └── includes/
│   │           └── event_card.html
│   ├── urls.py
│   └── views.py
│
├── models/                    # предметные классы (ПР3)
│   ├── __init__.py
│   ├── participants.py
│   ├── events.py
│   └── tickets.py
│
├── sql/                       # SQL-скрипты (ПР7)
│   ├── schema.sql             # Создание таблиц
│   └── queries.sql            # 10 SQL-запросов
│
├── db/                        # Работа с БД (ПР7)
│   ├── __init__.py
│   ├── database.py            # Подключение к SQLite
│   └── import_json.py         # Перенос данных из JSON
│
├── data/                      
│   ├── conference.sqlite      # Файл базы данных (ПР7)
│   ├── participants.json      # Исходные данные
│   ├── events.json            # Исходные данные
│   └── tickets.json           # Исходные данные
│
└── tests/                     # тесты предметной области
    ├── test_participants.py
    ├── test_events.py
    └── test_tickets.py
```

## 5. Веб-интерфейс

Веб-часть приложения реализована на Django. Основные страницы:

- `/` — главная страница;
- `/participants/` — список участников;
- `/participants/<id>/` — информация об участнике;
- `/events/` — список мероприятий;
- `/events/<id>/` — информация о мероприятии;
- `/events/search_events/` — поиск мероприятий по названию и дате;
- `/events/statistics/` — статистика по билетам;
- `/tickets/` — список билетов;
- `/events/tickets_paginated/` — список билетов с пагинацией;
- `/events/tickets_active/` — активные билеты (без отменённых);
- `/events/tickets_by_event_status/` — фильтрация билетов по мероприятию
  и статусу.

Для формирования страниц используются **Django-шаблоны**. Генерация HTML
непосредственно в Python-коде веб-представлений не используется:
view-функции подготавливают контекст и вызывают `render()`.
## 6. Django Template Language

Шаблоны используют возможности Django Template Language.

### 6.1. Базовый шаблон

Общий шаблон всех страниц: `templates/base.html`.

Он содержит HTML-структуру страницы, подключение Bootstrap и собственного
CSS, логотип, навигацию, футер и два блока:

```django
{% block title %}{% endblock %}
{% block content %}{% endblock %}
```

Дочерние шаблоны наследуют его:

```django
{% extends "base.html" %}
```

### 6.2. Включаемые шаблоны

Повторяющиеся фрагменты вынесены в отдельные шаблоны:

- `includes/navigation.html` — навигационное меню;
- `participants/includes/participant_card.html` — карточка участника;
- `events/includes/event_card.html` — карточка мероприятия.

Подключение выполняется через:

```django
{% include "includes/navigation.html" %}
{% include "participants/includes/participant_card.html" %}
{% include "events/includes/event_card.html" %}
```

### 6.3. Контекст

View-функции передают данные в шаблоны через словарь контекста:

```python
context = {
    "participants": participants_list,
}
return render(request, "participants/participant_list.html", context)
```

В шаблоне данные доступны по имени переменной:

```django
{% for participant in participants %}
    ...
{% endfor %}
```

Аналогично передаются `events` и `tickets`.

### 6.4. Циклы и условия

Для перебора коллекций используется:

```django
{% for participant in participants %}
    ...
{% empty %}
    <li class="list-group-item">Участники не найдены.</li>
{% endfor %}
```

Для условного отображения — конструкция `{% if %}`. Например,
на странице детали проверяется, найден ли объект:

```django
{% if participant %}
    ...
{% else %}
    <h1 class="text-danger">Участник не найден</h1>
{% endif %}
```

### 6.5. Фильтры шаблонов

В шаблонах используются стандартные фильтры Django:

- количество мероприятий: `{{ events|length }}`;
- значение по умолчанию: `{{ event.title|default:"Без названия" }}`.

Фильтры используются только для представления данных и не содержат
бизнес-логику приложения.

### 6.6. URL-маршрутизация

Для страниц используются именованные маршруты с пространствами имён:

```django
{% url 'homepage:index' %}
{% url 'participants:participants' %}
{% url 'participants:participant_detail' participant.id %}
{% url 'events:events' %}
{% url 'events:event_detail' event.id %}
{% url 'events:search_events' %}
{% url 'events:statistics' %}
{% url 'tickets' %}
{% url 'events:tickets_paginated' %}
{% url 'events:tickets_active' %}
{% url 'events:tickets_by_event_status' %}
```

Для приложений заданы app_name (homepage, participants, events),
что позволяет обращаться к маршрутам через app:name. Ссылки в шаблонах
формируются через {% url %}, жёстко заданные адреса не используются.

## 7. Статические файлы

Статические файлы находятся в:

```
homepage/static/homepage/
├── css/style.css
├── js/main.js
└── img/logo.webp
```

В шаблонах используется тег `{% load static %}` и конструкция
`{% static '...' %}`:

```django
<link rel="stylesheet" href="{% static 'homepage/css/style.css' %}">
<img src="{% static 'homepage/img/logo.webp' %}" alt="Логотип">
<script src="{% static 'homepage/js/main.js' %}"></script>
```

В проекте есть собственный CSS (`style.css`) для оформления карточек
и логотипа. JavaScript (`main.js`) автоматически подставляет текущий год
в футер страницы. Bootstrap 5.3 сохранён для базовой вёрстки.

## 8. Хранение данных

Данные приложения хранятся в реляционной базе данных SQLite: `db.sqlite3` (управляется Django ORM).

- Модели: `Participant` (`participants/models.py`), `Event` и `Ticket` (`events/models.py`).
- Связи: `Ticket.event` → `Event`, `Ticket.participant` → `Participant` (ForeignKey, `on_delete=CASCADE`, `related_name='tickets'`).
- Миграции: `participants/migrations/`, `events/migrations/`.
- Перенос данных из ПР7 (`data/conference.sqlite`) выполнен скриптом `db/migrate_to_orm.py`.
- Представления получают данные через Django ORM (`objects.all()`, `filter()`, `exclude()`, `select_related()`, `annotate()`, `aggregate()`, `Paginator`).
- Исходные JSON-файлы (`data/*.json`) и база ПР7 (`data/conference.sqlite`) сохранены как исходные данные.
- SQL-слой ПР7 (`sql/schema.sql`, `sql/queries.sql`, `db/database.py`) остаётся в проекте как предыдущая реализация, но представления его больше не используют.

## 8.1. ORM-запросы проекта (ПР9)
В представлениях используются:

- базовое получение: Event.objects.all(), get_object_or_404(Event, pk=...);
- фильтрация: filter(date=...), filter(title__icontains=...), filter(event__title__icontains=...), exclude(status='отменён'), filter(status__in=[...]);
- поиск: filter(title__icontains=...), filter(Q(name__icontains=...) | Q(email__icontains=...));
- сортировка: order_by('date'), order_by('date', 'title'), order_by('event__date', 'participant__name');
- работа со связями: select_related('event', 'participant'), event.tickets.all(), participant.tickets.all();
- агрегирование и аннотирование: annotate(Count('tickets')), aggregate(Count, Avg, Min, Max), aggregate(Sum('registered'));
- пагинация: Paginator(tickets_qs, 5) + get_page.

## 9. Основные модули

- `storage.py` — загрузка и сохранение данных в JSON;
- `models/` — классы предметной области Participant, Event, Ticket;
- `participants/models.py` — Django-модель Participant (ПР9);
- `events/models.py` — Django-модели Event, Ticket (ПР9);
- `db/migrate_to_orm.py` — перенос данных из SQLite в Django ORM (ПР9);
- `main.py` — консольная версия приложения (сохранена с ПР3);
- `utils.py` — вспомогательные функции для консольного ввода;
- `homepage/views.py` — представление главной страницы;
- `participants/views.py` — обработка запросов по участникам (ORM);
- `events/views.py` — обработка запросов по мероприятиям и билетам (ORM).

## 10. Тестирование

В каталоге `tests/` находятся тесты основных классов предметной области:

```
tests/
├── test_participants.py
├── test_events.py
└── test_tickets.py
```

Запуск тестов:

```bash
pytest -v
```

## 11. Проверка качества кода

Проверка кода линтером flake8:

```bash
flake8 . --extend-exclude=venv
```

## 12. Запуск проекта

Перед запуском активировать виртуальное окружение:

```bash
source venv/Scripts/activate
```

Применить миграции (один раз):

```bash
python manage.py migrate
```

Запустить сервер разработки:

```bash
python manage.py runserver
```

Веб-интерфейс доступен по адресу:

```
http://127.0.0.1:8000/
```

Консольная версия запускается отдельно:

```bash
python main.py
```

## 13. Работа с Git

Исходный код проекта хранится в Git-репозитории. Изменения фиксируются
по этапам, сообщения коммитов начинаются с метки практической работы.

Пример:

```bash
git status
git add .
git commit -m "PR6: add Django templates and static files"
git push
```

## 14. Текущее состояние проекта

На текущем этапе проект содержит:

- предметные классы Participant, Event, Ticket (пакет models/);
- консольный интерфейс;
- Django-проект и три Django-приложения (homepage, participants, events);
- Django-модели Participant, Event, Ticket и связи между ними;
- миграции (participants/migrations/, events/migrations/);
- перенос данных из data/conference.sqlite в db.sqlite3 (скрипт db/migrate_to_orm.py);
- веб-представления для основных сущностей на Django ORM;
- Django Template Language;
- наследование шаблонов;
- базовый шаблон base.html;
- блоки {% block %};
- включаемые шаблоны через {% include %};
- циклы и условия;
- фильтры шаблонов;
- именованные URL и пространства имён;
- статические файлы (CSS, JavaScript, изображение);
- собственное оформление интерфейса;
- тесты предметной области;
- ORM-запросы: получение наборов и отдельных объектов, фильтрация,
поиск, сортировка, работа со связями, агрегирование, пагинация;
- страница поиска мероприятий по названию и дате;
- страница статистики по билетам со сводными показателями;
- страница билетов с пагинацией;
- страница активных билетов (без отменённых);
- страница фильтрации билетов по мероприятию и статусу;
- SQL-слой ПР7 (sql/schema.sql, sql/queries.sql, db/database.py)
сохранён как предыдущая реализация.

## 15. Дальнейшее развитие

На текущем этапе слой доступа к данным переведён на Django ORM: модели, миграции, ORM-запросы (фильтрация, поиск, сортировка, агрегация, пагинация). Следующие этапы предполагают реализацию форм Django для создания и редактирования записей, обработку пользовательского ввода, валидацию данных и, возможно, API.