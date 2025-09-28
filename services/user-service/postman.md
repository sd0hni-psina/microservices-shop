# Руководство по тестированию Django User Service в Postman

## Подготовка к тестированию

### 1. Запуск сервиса
```bash
cd services/user-services
python manage.py migrate
python manage.py runserver
```

### 2. Настройка Postman
- Создайте новую коллекцию "Django User Service"
- Установите базовый URL: `http://127.0.0.1:8000`

## Тестовые сценарии

### 1. Регистрация пользователя

**Endpoint:** `POST /api/users/register/`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "email": "test@example.com",
    "username": "testuser",
    "first_name": "Test",
    "last_name": "User",
    "password": "password123",
    "password_confirm": "password123"
}
```

**Ожидаемый ответ (201 Created):**
```json
{
    "id": 1,
    "email": "test@example.com",
    "username": "testuser",
    "first_name": "Test",
    "last_name": "User"
}
```

**Негативные тесты:**
1. **Несовпадающие пароли:**
```json
{
    "email": "test2@example.com",
    "username": "testuser2",
    "first_name": "Test",
    "last_name": "User",
    "password": "password123",
    "password_confirm": "differentpassword"
}
```

2. **Дублирующийся email:**
```json
{
    "email": "test@example.com",
    "username": "testuser3",
    "first_name": "Another",
    "last_name": "User",
    "password": "password123",
    "password_confirm": "password123"
}
```

### 2. Авторизация пользователя

**Endpoint:** `POST /api/auth/login/`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "email": "test@example.com",
    "password": "password123"
}
```

**Ожидаемый ответ (200 OK):**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
        "id": 1,
        "email": "test@example.com",
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User"
    }
}
```

**Негативные тесты:**
1. **Неверные данные:**
```json
{
    "email": "test@example.com",
    "password": "wrongpassword"
}
```
Ожидаемый ответ: `401 Unauthorized`

2. **Пустые поля:**
```json
{
    "email": "",
    "password": ""
}
```
Ожидаемый ответ: `400 Bad Request`

### 3. Обновление токена

**Endpoint:** `POST /api/auth/refresh/`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "refresh": "ваш_refresh_token_из_предыдущего_запроса"
}
```

**Ожидаемый ответ (200 OK):**
```json
{
    "access": "новый_access_token"
}
```

### 4. Просмотр профиля (требует авторизации)

**Endpoint:** `GET /api/users/profile/`

**Headers:**
```
Authorization: Bearer ваш_access_token
Content-Type: application/json
```

**Ожидаемый ответ (200 OK):**
```json
{
    "phone": "",
    "address": "",
    "date_of_birth": null
}
```

### 5. Обновление профиля (требует авторизации)

**Endpoint:** `PUT /api/users/profile/update/`

**Headers:**
```
Authorization: Bearer ваш_access_token
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "phone": "+7 777 123 4567",
    "address": "г. Атырау, ул. Примерная, 123",
    "date_of_birth": "1990-01-15"
}
```

**Ожидаемый ответ (200 OK):**
```json
{
    "phone": "+7 777 123 4567",
    "address": "г. Атырау, ул. Примерная, 123",
    "date_of_birth": "1990-01-15"
}
```

## Настройка переменных окружения в Postman

Создайте environment со следующими переменными:

```
base_url: http://127.0.0.1:8000
access_token: (будет автоматически заполняться после логина)
refresh_token: (будет автоматически заполняться после логина)
```

## Автоматизация с помощью Tests в Postman

### Для запроса логина добавьте следующий скрипт в Tests:

```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response has tokens", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('access');
    pm.expect(jsonData).to.have.property('refresh');
    
    // Сохраняем токены в переменные окружения
    pm.environment.set("access_token", jsonData.access);
    pm.environment.set("refresh_token", jsonData.refresh);
});
```

### Для запросов, требующих авторизации, в Headers используйте:

```
Authorization: Bearer {{access_token}}
```

## Создание коллекции для Postman

1. **Создайте новую коллекцию** "Django User Service"

2. **Добавьте папки:**
   - Authentication
   - User Management
   - Profile Management

3. **Расположите запросы по папкам:**

**Authentication:**
- Login User
- Refresh Token

**User Management:**
- Register User

**Profile Management:**
- Get Profile
- Update Profile

## Последовательность тестирования

1. **Регистрация нового пользователя**
2. **Авторизация пользователя** (сохранение токенов)
3. **Просмотр профиля**
4. **Обновление профиля**
5. **Обновление токена**
6. **Тестирование с невалидными данными**

## Дополнительные проверки

### Проверка статус-кодов:
- 200: Успешный запрос
- 201: Объект создан
- 400: Ошибка валидации
- 401: Неавторизованный доступ
- 404: Объект не найден

### Проверка структуры ответов:
- Все обязательные поля присутствуют
- Типы данных соответствуют ожидаемым
- Токены имеют корректный формат JWT

## Дополнительные возможности

### Runner для автоматического тестирования:
1. Выберите коллекцию
2. Нажмите "Run collection"
3. Настройте порядок выполнения запросов
4. Запустите полное тестирование

### Экспорт результатов:
- Экспортируйте коллекцию для передачи команде
- Настройте CI/CD интеграцию через Newman

Это руководство поможет вам комплексно протестировать все функции вашего Django сервиса пользователей.