# Отслеживание проверки заданий
Скрипт

### Как установить
Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:

```sh
pip install -r requirements.txt
```
#### Необходимые данные

Проект GoogleCloud
Для получения доступа к агенту DialogFlow, необходима создать проект GoogleCloud, см. документацию https://cloud.google.com/dialogflow/es/docs/quick/setup
 - учетная запись Google
 - создать проект (далее переменная окружения `PROJECT_GOOGLE_CLOUD_ID`)
 - включить API
 - настройка аутентификации (переменная окружения путь `GOOGLE_APPLICATION_CREDENTIALS` к файлу `application_default_credentials.json`) см. документацию https://cloud.google.com/dialogflow/es/docs/quick/setup
 - создать API key с помощью скрипта `create_api_key.py` (ключ создается без ограничений, для полной безопасности добавьте ограничения) см. документацию https://cloud.google.com/docs/authentication/api-keys
```sh
python create_api_key.py
```
Агент DialogFlow
Для обработки естественного языка и обучения используется облачная платформа от Google Dialogflow https://dialogflow.cloud.google.com/
 - учетная запись Google (использовать учетную предыдущего шага GoogleCloud)
 - создать агента (с использованием id проекта GoogleCloud `PROJECT_GOOGLE_CLOUD_ID`) см. документацию https://cloud.google.com/dialogflow/es/docs/quick/build-agent
 - указать язык обработчика (далее переменная окружения `LANGUAGE_CODE`)
 - создать новое намерение (intent) 

#### Переменные окружения:

Часть настроек проекта берётся из переменных окружения. Чтобы их определить, создайте файл `.env` в корневом каталоге и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.

```
.
├── .env
└── main.py
```
Обязательные переменные окружения:
- `TELEGRAM_TOKEN` - токен выглядит например: `6000000001:ADEeVTKrhmLSBouDAjhT0r9tBG-AW5VU9YG`. См. документацию https://core.telegram.org/bots/faq#how-do-i-create-a-bot
- `TELEGRAM_CHAT_ID` - (бот для уведомлений) выглядит например: `1000001234567` Напишите в Telegram специальному боту: https://telegram.me/userinfobot
- `PROJECT_GOOGLE_CLOUD_ID` - id приложения GoogleCloud: `ru-RU` См. документацию https://cloud.google.com/dialogflow/es/docs/quick/build-agent
- `GOOGLE_APPLICATION_CREDENTIALS` - путь к файлу `application_default_credentials.json`, см. документацию https://cloud.google.com/dialogflow/es/docs/quick/setup
- `LANGUAGE_CODE` - язык обработки запросов агента DialogFlow: `ru-RU` См. документацию https://cloud.google.com/dialogflow/es/docs/quick/build-agent
- `VK_TOKEN` - токен выглядит например: `vk1.a.XxBH4zwP0Ak7vdiSpKWRH6FwWE59LuwTnoFHsReYRt9tQmtiRYrLwyb9kylLp27YHninApFuyRi-MLMXtSnV6Bb3nCutvq27jCv82Yn6bKbeDsVCfhQi3gxxSXKxWslNROWFWyN7S3pDWUqscB5OX_wXXtdMn_p4KE-9nUeWaKr-2uCo2Yyj65_4IAmT9jZ0NKKxPfnnxsxkAHsJho33uw`. См. документацию https://dev.vk.com/ru/api/access-token/community-token/in-community-settings


### Применение
Скрипт работает из консольной утилиты.

Для запуска скрипта:
```sh
python main.py
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
