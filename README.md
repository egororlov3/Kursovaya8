# Название проекта

Отслеживание полезных привычек + интеграция с ТГ ботом.

## Установка

### Предварительные требования

- [Docker](https://www.docker.com/get-started) 
- [Docker Compose](https://docs.docker.com/compose/install/)

### Клонирование репозитория

1. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/egororlov3/Kursovaya8.git
   ```
   
2. Соберите и запустите контейнеры:
   ```bash
   docker-compose up --build
   ```

3. После запуска, получите доступ к приложению через браузер:
   ```bash
   http://localhost:8000
   ```
   
### Запуск миграций

После первого запуска необходимо выполнить миграции базы данных:
 ```bash
   docker-compose exec web python manage.py migrate
   ```

