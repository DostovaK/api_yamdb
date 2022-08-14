# YaMDb

## Описание проекта

Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен администратором.

Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

Произведению может быть присвоен жанр (Genre) из списка предустановленных. Новые жанры может создавать только администратор.

Пользователи оставляют к произведениям текстовые отзывы (Review) и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.

&ensp;

## Как запустить проект

 Клонировать репозиторий и перейти в него в командной строке:

``` bash
git clone git@github.com:DostovaK/api_yamdb.git
```

``` bash
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

``` bash
python3 -m venv venv
```

``` bash
source venv/bin/activate
```

``` bash
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

``` bash
pip install -r requirements.txt
```

Выполнить миграции:

``` bash
python3 manage.py migrate
```

Запустить проект:

``` bash
python3 manage.py runserver
```

&ensp;

## Примеры запросов к API

### Регистрация нового пользователя. Код подтвержения отправляется на переданный email

POST `api/v1/auth/signup/`

``` JSON
{
    "username": "test_user",
    "email": "test@mail.ru"
}
```

Ответ:

``` JSON
{
    "email": "test@mail.ru",
    "username": "test_user"
}
```

&nbsp;

### Получение JWT-токена

POST `api/v1/auth/token/`

``` JSON
{
    "username": "test_user",
    "confirmation_code": "639-c134f9e28fb1ada9c58a"
}
```

Пример ответа:

``` JSON
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjYwMzg1NzIzLCJqdGkiOiIyODliNDM1MTA1YjQ0MDNiOTE3ZTViM2U0NjQwMGE2OSIsInVzZXJfaWQiOjV9.PX9SWNxRi-bAGIPzc3p_PI8l565SrJIuzCLZxYyo"
}
```

&nbsp;

### Получение списка всех категорий

GET  `api/v1/categories/`

Пример ответа:

``` JSON

```

&nbsp;

### Получение информации о произведении

GET `api/v1/titles/{titles_id}/`

Пример ответа:

``` JSON

```

&nbsp;

### Добавление комментария к отзыву

POST `api/v1/titles/{title_id}/reviews/{review_id}/comments/`

``` JSON

```

Пример ответа:

``` JSON

```
