# Проект Яндекс Лицей
### Программа для моделирования библиотеки с сипользованием фреймворка Flask

Получение:  
git clone https://github.com/vzaletny/school_library.git

Установка:
* Системый Python: 
  ```bash
  cd school_library
  pip install -r requirements.txt
  ```
* Виртуальное окружение venv для Windows
  ```bash
  cd school_library
  python -m venv venv
  venv/Scripts/activate
  pip install -r requirements.txt
  ```
* Виртуальное окружение venv для Linux
  ```bash
  cd school_library
  python -m venv venv
  . venv/Scripts/activate
  pip install -r requirements.txt
  ```
    
* Виртуальное окружение pipenv
  ```bash
  cd school_library
  pip install pipenv
  pipenv sync
  ```
  
Запуск:
* Windows:
  + ```bash
    python run.py
    ```
  + ```bash
    set FLASK_APP=library.py
    flask run
    ```
  + ```bash
    set FLASK_APP=library.py
    pipenv run flask run
    ```
* Linux:
  + ```bash
    python run.py
    ```
  + ```bash
    export FLASK_APP=library.py
    flask run
    ```
  + ```bash
    export FLASK_APP=library.py
    pipenv run flask run
    ```

RESTful API
GET запрос - можно выполнить из любого браузера
* Получить список объектов User
```bash
  http://server_name:port/api/users
```
* Получить конкретный объект User по user ID
```bash
  http://server_name:port/api/users/1
```
* Получить список выданных книг и их авторов в разрезе пользователей
```bash
  http://server_name:port/api/orders
```
* Получить список выданных книг и их авторов для конкретного объекта User по user ID
```bash
  http://server_name:port/api/orders/1
```
Для выполнеия запросов POST, PUT и DELETE необходимо установить API testing tool.  
Advanced REST Client (ARC) - https://install.advancedrestclient.com/install  
Postman - https://www.postman.com/product/api-client/  
В заголовках запросов указать тип содержимого:   
```content-type: application/json```

Да удобного просмотра результатов запросов RESful API можно установть расширение для браузера  
https://chrome.google.com/webstore/detail/json-formatter/bcjindcccaagfpapjjmafapmmgkkhgoa?hl=ru
или временно включить режим отладки при запуске приложения на Flask в фале run.py
```bash
    if __name__ == '__main__':
        app.run(debug=True)
```
или с помощью установки переменной окружения FLASK_DEBUG=1
* Windows
  + ```bash
    set FLASK_DEBUG=1
    ```
* Linux
  + ```bash
    export FLASK_DEBUG=1
    ```
    
Формат объекта JSON для PUT/POST запросов  
```json
  {
    "first_name": "Ivan",
    "last_name": "Ivanov",
    "email": "i.ivanov@yandex.ru",
    "is_admin": false,
    "password_hash": "12345" 
  }
```