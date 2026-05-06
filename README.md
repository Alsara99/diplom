# 🧠 Task Tracker API

Серверное приложение для управления задачами сотрудников. Позволяет отслеживать загрузку сотрудников, управлять задачами и выявлять критически важные задачи, требующие назначения исполнителя.

---

## 🚀 Технологии

* Python 3.11+
* Django 5
* Django REST Framework
* PostgreSQL
* Docker / Docker Compose
* Swagger / ReDoc (drf-yasg)

---

## 📦 Функциональность

### 🔹 CRUD операции

Реализованы для:

* сотрудников (Workers)
* задач (Tasks)

Поддерживаются:

* создание
* получение списка
* получение одного объекта
* обновление
* удаление

---

### 🔹 Специальные эндпоинты

#### 📊 Занятые сотрудники

Возвращает список сотрудников с их активными задачами, отсортированный по количеству активных задач (по убыванию).

**GET**

```
/api/tracker/busy_workers/
```

---

#### ⚠️ Важные задачи

Возвращает список задач, которые:

* **не активны**
* но имеют зависимые задачи, которые уже **активны**

Также подбирается рекомендуемый исполнитель:

* наименее загруженный сотрудник
* или сотрудник, выполняющий зависимую задачу (если его загрузка не превышает минимум более чем на 2 задачи)

**GET**

```
/api/tracker/necessary_tasks/
```

**Формат ответа:**

```json
[
  {
    "task": "Название задачи",
    "deadline": "2026-05-10T12:00:00Z",
    "worker": "Иван Иванов"
  }
]
```

---

## 🔌 API эндпоинты

### 👷 Сотрудники

| Метод     | URL                                |
| --------- | ---------------------------------- |
| GET       | `/api/tracker/workers/`            |
| GET       | `/api/tracker/worker/{id}/`        |
| POST      | `/api/tracker/worker/new/`         |
| PUT/PATCH | `/api/tracker/worker/{id}/edit/`   |
| DELETE    | `/api/tracker/worker/{id}/delete/` |

---

### 📋 Задачи

| Метод     | URL                              |
| --------- | -------------------------------- |
| GET       | `/api/tracker/tasks/`            |
| GET       | `/api/tracker/task/{id}/`        |
| POST      | `/api/tracker/task/new/`         |
| PUT/PATCH | `/api/tracker/task/{id}/edit/`   |
| DELETE    | `/api/tracker/task/{id}/delete/` |

---

## 🐳 Запуск через Docker

### 1. Создать `.env` файл

На основе `.env.template`:

```
DB_NAME=your_db
DB_USER=your_user
DB_PASSWORD=your_password
```

---

### 2. Запуск

```bash
docker-compose up --build
```

---

### 3. Приложение будет доступно:

* API: http://localhost:8003/api/tracker/
* Swagger: http://localhost:8003/swagger/
* ReDoc: http://localhost:8003/redoc/

---

## ⚙️ Локальный запуск (без Docker)

```bash
python -m venv venv
source venv/bin/activate  # или venv\Scripts\activate на Windows

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

---

## 🧪 Тестирование

```bash
python manage.py test
```

---

## 📁 Структура проекта

```
diplom/
├── config/         # настройки Django
├── tracker/        # основное приложение
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   ├── tests.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── manage.py
```

---

## ✅ Валидация данных

Используется Django REST Framework:

* проверка типов данных
* обязательные поля
* бизнес-логика (например, корректность статусов)

---

## 📖 Документация API

Автоматически генерируется:

* Swagger: `/swagger/`
* ReDoc: `/redoc/`

---

## 🧠 Особенности реализации

* Используется `annotate + Count` для подсчёта нагрузки сотрудников
* `prefetch_related` для оптимизации запросов
* Логика выбора исполнителя для важных задач учитывает текущую загрузку

---

## 📌 Требования

* Docker
* Docker Compose

или

* Python 3.11+
* PostgreSQL
