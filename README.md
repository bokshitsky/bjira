
# bjira - утилита для упрощения взаимодействия с jira из консоли

## Как пользоваться

1. Склонировать репу.

2. Установить тулзу:

```shell script
~ » python3 setup.py install
```

3. В home-папку положить файл с конфигом со своими данными:

```shell script
~ » cat .bjira_config
```

```json5
{
  "host": "https://jira.hh.ru",
  "user": "user-name",
  "team": "team-name"
}
```

4. Установить пароль

```shell script
~ » bjira setpass
```

5. Использовать

```shell script
~ » bjira create -s 'xmlback' -m 'NEW TASK NAME'            # HH задача "[xmlback] NEW TASK NAME"

~ » bjira create -m 'NEW TASK NAME'                         # HH задача "NEW TASK NAME"

~ » bjira create -p 12345 -s 'xmlback' -m 'NEW TASK NAME'   # HH задача "[xmlback] NEW TASK NAME" прилинкованная к PORTFOLIO-12345

~ » bjira create at -m 'NEW TASK NAME'                      # AT задача "[at] NEW TASK NAME"

~ » bjira create at -p 12345 -m 'NEW TASK NAME'             # AT задача "[at] NEW TASK NAME" прилинкованная к PORTFOLIO-12345

~ » bjira create at -p 'PORTFOLIO-12345' -m 'NEW TASK NAME' # AT задача "[at] NEW TASK NAME" прилинкованная к PORTFOLIO-12345

~ » bjira create bg -m 'NEW BUG NAME'                       # bug-задача "NEW TASK NAME"

~ » bjira create bug -m -s xmlback 'NEW BUG NAME'           # bug-задача "[xmlback] NEW TASK NAME"

~ » bjira stas 11215              # Заполнить галочку про безопасность в PORTFOLIO-11215

~ » bjira stas P11215             # Заполнить галочку про безопасность в PORTFOLIO-11215

~ » bjira open HH-12345           # Открыть задачку или портфель в дефолтном браузере

~ » bjira open                    # Открыть задачку в браузере, имя задачки взять из ветки гит-репозитория
```
