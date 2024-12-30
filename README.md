## Talking bot

В данном проекте реализованы Телеграмм и VK боты-автоответчики.  
Боты обучаемые, на базе сервиса DialogFlow от Google Cloud.

[Пример Телеграм бота](https://t.me/dvmn_verb_games_bot)  
[Пример VK бота](https://vk.com/club228848035)

### Установка

Python3 должен быть установлен версии **3.8+**. Проект тестировался на версии **3.11**.  
Используйте `pip` для установки зависимостей:
```
$ pip install -r requirements.txt
```
Для реализации проекта вам понадобится:  
Telegram бот. Создать можно через [@BotFather](https://t.me/BotFather).  
Бот токен выглядит так: `1234567890:XXXxx0Xxx-xxxX0xXXxXxx0X0XX0XXXXxXx`.

Cообщество в VK. Необходимо создать ключ доступа (Настройки - Работа с API) для работы с VK Api.  
VK токен выглядит так: `vk1.a.LP_x0xXXxXXxX0xXxxXxxx0_xx0...`.

Проект в [Google Cloud](https://console.cloud.google.com) и созданный агент на базе этого проекта в сервисе [DialogFlow](https://dialogflow.cloud.google.com).  
После создания служебной учетной записи (service account) в проекте, необходимо получить файл авторизации.  
Можно получить коммандой через утилиту `gcloud` из состава Google Cloud CLI:
```sh
$ gcloud iam service-accounts keys create keyfile.json --iam-account={name}@{project_id}.iam.gserviceaccount.com
```
Для создания и добавления фраз и ответов для ботов можно воспользоваться скриптом `create_intents.py`.  
Скрипт загружает данные из `json` файла в агент DialogFlow.
```
$ py create_intents.py path/to/questions.json
```
Без аргумента скрипт будет искать файл `questions.json` в тойже папке где и сам скрипт.  
После создания интентов необходимо обучить агент. Для этого в настройках агента, в разделе `ML settings` нажать кнопку `TRAIN`.

Структура `json` файла:
```
{
    "Тема 1": {
        "questions": [
            "Вопрос 1",
            "Вопрос 2",
            ...
        ],
        "answer": "Ответ"
    },
    "Тема 2": {
        "questions": [
            "Вопрос 1",
            "Вопрос 2",
            ...
        ],
        "answer": "Ответ"
    },
}
```

Конфиденциальные данные (токены, пароли) сохраните в файл .env  
Пример:
```
# Токен Теленрам бота
TG_BOT_TOKEN = "1234567890:XXXxx0Xxx-xxxX0xXXxXxx0X0XX0XXXXxXx"

# ID пользователья Телеграм для отправки сообщений мониторинга ботов
TG_CHAT_ID = "98765432"

# Путь к файлу авторизации на платформе Google Cloud
GOOGLE_APPLICATION_CREDENTIALS = "path/to/keyfile.json"

# ID проекта на платформе Google Cloud
GOOGLE_PROJECT_ID = "talking-bot-XXXXXX"

# Токен сообщества VK
VK_GROUP_TOKEN = "vk1.a.LP_x0xXXxXXxX0xXxxXxxx0_xx0..."
```

### Запуск

Запуск Телеграм бота:
```
$ py tg_bot.py
```
Запуск VK бота:
```
$ py vk_bot.py
```

Для постоянной работы скриптов можно выполнить деплой на сервере.  
При запуске и в случае ошибок ботов, пользователь указанный в `TG_CHAT_ID` будет уведомлен через Телеграм.

### Примеры работы

Пример корректной работы админки:

![image](https://github.com/user-attachments/assets/caadada5-6653-485e-a93d-5badd5468d4a)

Пример работы бота:

![example](https://github.com/user-attachments/assets/a97802c8-f1f1-46ad-b0ec-66bceb0a8916)


### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).