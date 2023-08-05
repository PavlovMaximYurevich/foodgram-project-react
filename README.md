# Foodgram  - социальная сеть для рецептов

### Сайт проекта
*https://foodgram-project.servemp3.com/*

*суперпользователь alex*

*пароль Admin12345*

### Описание проекта
 
В эту соц.сеть можно постить рецепты разных стран мира

 ### Стек, использованный при написании проекта:

 - **Python**
 + **Django**
 * **Nginx**
 * **Gunicorn**
 * **Docker**

### Как запустить проект: 


Клонировать репозиторий и перейти в него в командной строке: 


``` 

git clone <аккаунт репозитория>

```


*Linux и Mac: для всех команд после python добавляем цифру 3 (например python3)*

Перейти в директорию infra_sprint1/backend/

Cоздать и активировать виртуальное окружение: 


```ruby

python -m venv venv



source venv/bin/activate 

``` 




**Примеры запросов:**

**Пример регистрации пользователя:**

 

```ruby

https://foodgram-project.servemp3.com/api/users/

{
  "email": "vpupkin@yandex.ru",
  "username": "vasya.pupkin",
  "first_name": "Вася",
  "last_name": "Пупкин",
  "password": "Qwerty123"
}
 

```
 
**Аутентификация пользователя**

При успешном вводе получаем _Access_ токен


```ruby

https://foodgram-project.servemp3.com/api/auth/token/login/

{
  "password": "string",
  "email": "string"
}
```

**Все рецепты:**

```ruby

https://foodgram-project.servemp3.com/api/recipes/

{
  "count": 123,
  "next": "http://foodgram.example.org/api/recipes/?page=4",
  "previous": "http://foodgram.example.org/api/recipes/?page=2",
  "results": [
    {
      "id": 0,
      "tags": [
        {
          "id": 0,
          "name": "Завтрак",
          "color": "#E26C2D",
          "slug": "breakfast"
        }
      ],
      "author": {
        "email": "user@example.com",
        "id": 0,
        "username": "string",
        "first_name": "Вася",
        "last_name": "Пупкин",
        "is_subscribed": false
      },
      "ingredients": [
        {
          "id": 0,
          "name": "Картофель отварной",
          "measurement_unit": "г",
          "amount": 1
        }
      ],
      "is_favorited": true,
      "is_in_shopping_cart": true,
      "name": "string",
      "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
      "text": "string",
      "cooking_time": 1
    }
  ]
}
```

**Список покупок**

Можно скачать список в формате txt

https://foodgram-project.servemp3.com/api/recipes/download_shopping_cart/

