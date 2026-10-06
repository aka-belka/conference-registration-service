from django.http import HttpResponse


def page(title: str, content: str) -> str:
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
        "/dist/css/bootstrap.min.css"
    )
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{bootstrap}">
</head>
<body>
    <nav class="nav bg-light px-3 py-2 mb-3">
        <a class="nav-link" href="/">Главная</a>
        <a class="nav-link" href="/participants/">Участники</a>
        <a class="nav-link" href="/events/">Мероприятия</a>
        <a class="nav-link" href="/tickets/">Билеты</a>
    </nav>
    <main class="container">{content}</main>
</body>
</html>"""


def page_not_found(request, exception):
    content = """
    <h1 class="text-danger">404 — страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(
        page("404 — страница не найдена", content),
        status=404,
    )


def index(request):
    content = """
    <h1 class="display-4">Сервис регистрации участников конференции</h1>
    <p class="lead">Управление участниками, мероприятиями и билетами.</p>
    <p>Основные разделы:</p>
    <a href="/participants/" class="btn btn-primary me-2">Участники</a>
    <a href="/events/" class="btn btn-success me-2">Мероприятия</a>
    <a href="/tickets/" class="btn btn-secondary">Билеты</a>
    """
    return HttpResponse(page("Сервис регистрации", content))
