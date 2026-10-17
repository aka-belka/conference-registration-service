# Сервис регистрации участников конференции

Учебное веб-приложение на Django для управления участниками конференции,
мероприятиями и билетами.

## 1. Назначение проекта

Сервис регистрации участников конференции — учебное приложение, которое
позволяет хранить сведения об участниках, мероприятиях и билетах,
выполнять основные операции с этими объектами и предоставлять доступ
к информации через веб-интерфейс на Django.

Проект развивается поэтапно: консольная версия приложения (ПР1–ПР3)
дополнена веб-интерфейсом (ПР5) и переведена на систему шаблонов Django (ПР6).

## 2. Используемые технологии

- Python 3;
- Django 5.2;
- Django Template Language (DTL);
- HTML5;
- CSS3;
- JavaScript;
- Bootstrap 5.3;
- JSON для хранения данных;
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
`Participant`, `Event` и `Ticket` (пакет `models/`).

На текущем этапе данные хранятся в JSON-файлах. Django ORM и база данных
приложения пока не используются.

## 4. Структура проекта

```
conference-registration-service/
│
├── README.md
├── requirements.txt
├── manage.py
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
├── data/                      # JSON-хранилище
│   ├── participants.json
│   ├── events.json
│   └── tickets.json
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
- `/tickets/` — список билетов.

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
{% url 'tickets' %}
```

Для приложений заданы `app_name` (`homepage`, `participants`, `events`),
что позволяет обращаться к маршрутам через `app:name`. Ссылки в шаблонах
формируются через `{% url %}`, жёстко заданные адреса не используются.

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

На текущем этапе данные приложения хранятся в JSON-файлах:

- `data/participants.json`;
- `data/events.json`;
- `data/tickets.json`.

Загрузка данных выполняется функциями модуля `storage.py`.
Предметные объекты создаются на основе собственных Python-классов
из пакета `models/`.

**Django ORM на текущем этапе не используется.** Работа с моделями Django
и базой данных относится к следующим практическим работам.

## 9. Основные модули

- `storage.py` — загрузка и сохранение данных в JSON;
- `models/` — классы предметной области `Participant`, `Event`, `Ticket`;
- `main.py` — консольная версия приложения (сохранена с ПР3);
- `utils.py` — вспомогательные функции для консольного ввода;
- `homepage/views.py` — представление главной страницы;
- `participants/views.py` — обработка запросов по участникам;
- `events/views.py` — обработка запросов по мероприятиям и билетам.

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

- предметные классы `Participant`, `Event`, `Ticket`;
- консольный интерфейс;
- хранение данных в JSON;
- Django-проект и три Django-приложения (`homepage`, `participants`, `events`);
- веб-представления для основных сущностей;
- Django Template Language;
- наследование шаблонов;
- базовый шаблон `base.html`;
- блоки `{% block %}`;
- включаемые шаблоны через `{% include %}`;
- циклы и условия;
- фильтры шаблонов;
- именованные URL и пространства имён;
- статические файлы (CSS, JavaScript, изображение);
- собственное оформление интерфейса;
- тесты предметной области.

Формы Django, модели Django ORM и работа с базой данных в текущей версии
проекта не реализованы.

## 15. Дальнейшее развитие

Следующие этапы развития проекта предполагают переход от хранения данных
в JSON к использованию базы данных и Django ORM, а также реализацию
форм Django и дальнейшее расширение веб-интерфейса.

В дальнейшем веб-приложение может быть дополнено операциями создания,
изменения и удаления объектов, обработкой пользовательского ввода,
валидацией данных и API.