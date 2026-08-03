# О проекте

Бэкенд веб-приложения "управления командой", написанного на Python с использованием FastAPI, развертыванием PostgreSQL для хранения данных.

## Установка

1. Склонируйте репозиторий к себе на локальную машину
    ```https://github.com/ErkinBabayakov/TeamManagerFastAPI.git
    ```
2. Перейдите в папку с проектом
3. При необходимости создайте и активируйте виртуальное окружение
   ```
   python -m venv venv
   ```
   - Активация на Windows
   ```
   venv\Scripts\activate
   ```
   - macOS/Linux
   ```
   source venv/bin/activate
   ```
4. Установите необходимые зависимости, из файла `requirements.txt` командой :
   ```
   pip install -r requirements.txt
   ```
5. Создайте и выполните миграции
   ```
   alembic revision --autogenerate -m "make migration"
   ```
   ```
   alembic upgrade head
   ```
## Запуск

```
uvicorn app.main:app --reload
```