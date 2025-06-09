# Чат бот телеграм и vk для диалога.

Скрипт для диалога с пользователем в телеграм и вконтакте.

<div align="center">
  <img src='./work.gif' alt='Демонстрация'>
</div>

### Как установить

Python3 должен быть уже установлен.
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:

```sh
pip install -r requirements.txt
```

#### Необходимые данные

Проект GoogleCloud
Для получения доступа к агенту DialogFlow, необходима создать проект GoogleCloud, см.
документацию https://cloud.google.com/dialogflow/es/docs/quick/setup

- учетная запись Google
- создать проект (далее переменная окружения `PROJECT_GOOGLE_CLOUD_ID`)
- включить API
- настройка аутентификации (переменная окружения путь `GOOGLE_APPLICATION_CREDENTIALS` к файлу
  `application_default_credentials.json`) см. документацию https://cloud.google.com/dialogflow/es/docs/quick/setup
- создать API key с помощью скрипта `create_api_key.py` (ключ создается без ограничений, для полной безопасности
  добавьте ограничения) см. документацию https://cloud.google.com/docs/authentication/api-keys

Для запуска скрипта `create_api_key.py -my_suffix` измените `my_suffix` на желаемый, для получения помощи отправьте
параметры -h

```
\amazing_chat_bot> python create_api_key.py -h
usage: create_api_key.py [-h] [suffix]

Введите суффикс к названию ключа (например: amazing-chat-bot).

positional arguments:
  suffix      Суффикс к названию ключа

options:
  -h, --help  show this help message and exit

```

Запустите скрипт что-бы создать суффикс по умолчанию `amazing-chat-bot` или добавьте переменную окружения `SUFFIX`:

```sh
python create_api_key.py
```

Агент DialogFlow
Для обработки естественного языка и обучения используется облачная платформа от Google
Dialogflow https://dialogflow.cloud.google.com/

- учетная запись Google (использовать учетную предыдущего шага GoogleCloud)
- создать агента (с использованием id проекта GoogleCloud `PROJECT_GOOGLE_CLOUD_ID`) см.
  документацию https://cloud.google.com/dialogflow/es/docs/quick/build-agent
- указать язык обработчика (далее переменная окружения `LANGUAGE_CODE`)
- создать новое намерение (intent)

#### Переменные окружения:

Часть настроек проекта берётся из переменных окружения. Чтобы их определить, создайте файл `.env` в корневом каталоге и
запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.

```
.
├── .env
└── main.py
```

Обязательные переменные окружения:

- `TELEGRAM_TOKEN` - токен выглядит например: `6000000001:ADEeVTKrhmLSBouDAjhT0r9tBG-AW5VU9YG`. См.
  документацию https://core.telegram.org/bots/faq#how-do-i-create-a-bot
- `ERROR_TELEGRAM_TOKEN` - (бот для отправки ошибок) токен выглядит например:
  `6000000001:ADEeVTKrhmLSBouDAjhT0r9tBG-AW5VU9YG`. См.
  документацию https://core.telegram.org/bots/faq#how-do-i-create-a-bot
- `TELEGRAM_CHAT_ID` - (бот для уведомлений) выглядит например: `1000001234567` Напишите в Telegram специальному
  боту: https://telegram.me/userinfobot
- `PROJECT_GOOGLE_CLOUD_ID` - id приложения GoogleCloud: `ru-RU` См.
  документацию https://cloud.google.com/dialogflow/es/docs/quick/build-agent
- `GOOGLE_APPLICATION_CREDENTIALS` - путь к файлу `application_default_credentials.json`, см.
  документацию https://cloud.google.com/dialogflow/es/docs/quick/setup
- `VK_TOKEN` - токен выглядит например:
  `vk1.a.XxBH4zwP0Ak1eriSpKWRH6FwWE59LugTklFHsReYRt9tQehjRYrLwyb8kylLp27YHninApFuyRi-MLMXtSnV6Bb3nCutvq27jCv82Yn6bKbeDsVCfhQi3gxxSXKxWslNROWFWyN7S3pDWUqscB5OX_wXXtdMn_p4KE-9nUeWaKr-2uCo2Yyj65_4IAmT9jZ0NKKxPfnnxsxkAHsJho33uw`.
  См. документацию https://dev.vk.com/ru/api/access-token/community-token/in-community-settings

Не обязательные переменные окружения:

- `LANGUAGE_CODE` - язык обработки запросов агента DialogFlow: `ru-RU` (значение по умолчанию `ru-RU`). См.
  документацию https://cloud.google.com/dialogflow/es/docs/quick/build-agent
- `SUFFIX` - суффикс выглядит например: `amazing-chat-bot`. Используется при создании API key.
- `LOCAL_PATH` - путь к файлу c intent например: `intent/intents.json`. Используется при добавлении intent.

### Применение

Скрипт работает из консольной утилиты.

Для запуска бота Telegram используйте скрипт:

```sh
python tg_bot.py
```

Для запуска бота VK используйте скрипт:

```sh
python vk_bot.py
```

#### Добавить intent (намерения):

Для добавления intent можно воспользоваться скриптом `add_intent_dialogflow.py`
Необходим json файл установленного образца, см. пример `intent/intents.json`

Для запуска скрипта `add_intent_dialogflow.py -my_local_path` измените `my_local_path` на ваш путь к файлу с intent, для
получения помощи отправьте параметры -h

```
\amazing_chat_bot> python add_intent_dialogflow.py -h
usage: add_intent_dialogflow.py [-h] [local_path]

Введите путь к файлу c intent (намерения), например: intent/intents.json

positional arguments:
  local_path  Путь к файлу с intent

options:
  -h, --help  show this help message and exit

```

Запустите скрипт с путем к файлу intent по умолчанию `intent/intents.json` или добавьте переменную окружения
`LOCAL_PATH`:

```sh
python add_intent_dialogflow.py
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
