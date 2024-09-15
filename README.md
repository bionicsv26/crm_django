
# [crm django]() &middot; [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/facebook/react/blob/main/LICENSE)  [![Python](https://img.shields.io/badge/Python-3.10.12-brightgreen.svg)](https://www.python.org/downloads/) [![Django version](https://img.shields.io/badge/Django%20-4.2.10%20-brightgreen)](https://docs.djangoproject.com/en/4.2/)

Разработанная CRM-система для автоматизации работы с клиентами, включает операции по созданию, редактированию и удалению следующих компонентов:
* **Услуги**
* **Рекламные компании** 
* **Потенциальные клиенты**
* **Контракты**
* **Активные клиенты**

Функционально эти блоки разделены для работы с разными группами пользователей:
* маркетолог (ведет блоки *Услуги* и *Рекламные компании*)
* оператор (ведет блок *Потенциальные клиенты*)
* менеджер (ведет блоки *Контракты* и *Активные клиенты*)
* администратор (заводит пользователей посредством административной панели, включает их в соответствующие группы)

В системе ведется статистика успешности рекламных компаний, которая видна для всех групп пользователей


## Содержание
- [Технологии](#технологии)
- [Установка](#Установка)
- [Команда проекта](#команда-проекта)

## Технологии
- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/download/)
- [PostgreSQL](https://www.postgresql.org/download/)

## Установка

```bash
# Примеры команд указаны для linux

# Создать каталог в нужном месте и перейти в него.
mkdir crm && cd crm

# Создать виртуальное окружение и активировать.
 python3 -m venv venv
 source /home/....../crm/venv/bin/activate

# Клонировать удаленный репозиторий в одноименную директорию.
git clone https://github.com/bionicsv26/crm_django

# Перейти в каталог crm/crm_django/src и установить следующие параметры виртeального окружения:
export PYTHONPATH=$PWD
export DJANGO_SETTINGS_MODULE=crm.crm.settings

# Установить зависимости из requirements/base.txt
pip install ../requirements/base.txt

# В файле .env указать ваши параметры секретного ключа джанго и базы данных PostgreSQL
SECRET_KEY=####
POSTGRESQL_NAME=####
POSTGRESQL_USER=####
POSTGRESQL_PASSWORD=####
POSTGRESQL_PORT=####
```

## Команда проекта

- [@bionicsv26](https://github.com/bionicsv26)

### License

CRM is [MIT licensed](./LICENSE).
Licensed under the MIT, see [LICENSE](./LICENSE) for more information.