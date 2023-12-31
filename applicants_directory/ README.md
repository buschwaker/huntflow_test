# Тестовое задание на должность junior python-разработчик

## Задача

Перенести тестовую базу кандидатов из Экселя и файлов в Хантфлоу, используя [Хантфлоу API](https://dev-100-api.huntflow.dev/v2/docs). 
Данные для входа в Хантфлоу будут предоставлены вместе с заданием. Токены для API можно
сгенерировать в беб-интерфейсе Хантфлоу в настройках организации:
* меню в правом верхнем углу -> настройки -> на открывшейся странице настроек внизу есть раздел API

## Состав задачи

Есть файл с кандидатами `Тестовая база.xslx` с колонками.

Необходимо добавить в Хантфлоу кандидатов из этого файла в базу и на вакансию на соответствующий этап с комментарием (вакансии уже созданы в Хантфлоу).

Кроме этого, в папках с названием вакансии находятся резюме кандидатов, их также необходимо прикрепить к кандидату из Excel.

## Приемка задачи и оценка выполнения

Будет оцениваться качество переноса информации и ее полнота, понятность, корректность кода и его
соответствие принятым стандартам python (pep8).

Скрипт должен уметь принимать параметры командной строки:
* токен или путь к файлу с токенами
* путь к папке с базой

Плюсом будет умение скрипта запускать заливку с места последнего запуска (на случай сетевых проблем или прерывании выполнения), например, с определенной строки.


Также, плюсом будет ссылка на выполненное задание на GitHub.
