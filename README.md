## Клонируйте проект
``` git clone https://github.com/IgnatyKhramtsov/Analytical-service.git ```

## Установите зависимости проекта
``` pip install -r requirements.txt ```

## Задайте параметры базы данный в файле **.env** по шаблону внутри.

## Задать папку **src** как **Sources root**

## Запустите миграцию базы данных
``` alembic upgrade head ```

## Запустите проект из консоли, перейдя в папку **src**:
``` uvicorn main:app --reload ```

## Для запуска через Docker:
### - заполните файл **.env_non_dev** по шаблону
### - для запуска введите ``` docker-compose up --build ```

## Перейти по адресу: http://localhost:8001/