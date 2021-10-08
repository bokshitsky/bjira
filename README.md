
# bjira - утилита для упрощения взаимодействия с jira из консоли

## Как пользоваться

1. Склонировать репу.

2. Установить venv и зависимости:

```shell script
sudo rm -rf .venv
python3 -m venv `pwd`/.venv
source ./.venv/bin/activate
sudo python -m pip install -r requirements.txt
deactivate
```

3. Прописать alias в .bashrc / .zshrc
```shell script
echo 'alias bjira="'`pwd`'/.venv/bin/python '`pwd`'/run.py"' >> ~/.zshrc
```

4. Добавить файл .bjira_config в home папку
```   
{
    "host": "https://jira.hh.ru",
    "user": "твоё.имя",
    "team": "mobi-dick"
}
```

5. Установить пароль

```shell script
~ » bjira setpass
```

6. Использовать

```shell script
~ » bjira create -s 'xmlback' -m 'NEW TASK NAME'            # HH задача "[xmlback] NEW TASK NAME"

~ » bjira create -m 'NEW TASK NAME'                         # HH задача "NEW TASK NAME"

~ » bjira create -p 12345 -s 'xmlback' -m 'NEW TASK NAME' -sp 0.5   # HH задача "[xmlback] NEW TASK NAME" на 0.5sp прилинкованная к PORTFOLIO-12345

~ » bjira create at -m 'NEW TASK NAME'                      # AT задача "[at] NEW TASK NAME"

~ » bjira create at -p 12345 -m 'NEW TASK NAME'             # AT задача "[at] NEW TASK NAME" прилинкованная к PORTFOLIO-12345

~ » bjira create at -p 'PORTFOLIO-12345' -m 'NEW TASK NAME' # AT задача "[at] NEW TASK NAME" прилинкованная к PORTFOLIO-12345

~ » bjira create bg -m 'NEW BUG NAME'                       # bug-задача "NEW TASK NAME"

~ » bjira create bug -m -s xmlback 'NEW BUG NAME'           # bug-задача "[xmlback] NEW TASK NAME"

~ » bjira my                 # Показать последние задачи связанные со мной

~ » bjira my 15              # Показать последние 15 задач связанных со мной

~ » bjira stas 11215              # Заполнить галочку про безопасность в PORTFOLIO-11215

~ » bjira stas P11215             # Заполнить галочку про безопасность в PORTFOLIO-11215

~ » bjira view HH-12345           # Открыть задачку или портфель в дефолтном браузере

~ » bjira view                    # Открыть задачку в браузере, имя задачки взять из ветки гит-репозитория
```
