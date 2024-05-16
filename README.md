
# bjira - утилита для упрощения взаимодействия с jira из консоли

## Устанавливаем (варианты)

### Глобально (может не установиться без sudo, в зависимости от используемого python-а)

```shell
python -m pip install git+ssh://git@github.com/bokshitsky/bjira.git@master
```

### Через [pipx](https://github.com/pypa/pipx)

```shell
pipx install 'git+ssh://git@github.com/bokshitsky/bjira.git@master'
```

### В .venv с вызовом через simlink

```shell
python -m venv bjira_venv && bjira_venv/bin/python -m pip install 'git+ssh://git@github.com/bokshitsky/bjira.git@master'
sudo ln -s `pwd`/bjira_venv/bin/bjira /usr/local/bin/bjira
```

### В .venv с вызовом через simlink в локальном checkout-е репы (удобно для разработки самой bjira)

```shell
git clone git@github.com:bokshitsky/bjira.git && cd bjira && poetry install
sudo ln -s `pwd`/.venv/bin/bjira /usr/local/bin/bjira
```

### В .venv с вызовом через alias

```shell
python -m venv bjira_venv && bjira_venv/bin/python -m pip install 'git+ssh://git@github.com/bokshitsky/bjira.git@master'
echo "alias bjira=$PWD/bjira_venv/bin/bjira" >> ~/.zshrc
```

## Как пользоваться

### Добавить файл .bjira_config в home папку

```shell script
cat <<EOF > ~/.bjira_config
{
    "host": "https://jira.hh.ru",
    "user": "твоё.имя",
    "team": "mobi-dick"
}
EOF
```

### Установить пароль

```shell script
bjira setpass
```

### Использовать

```shell script
~ » bjira create -s 'xmlback' -m 'NEW TASK NAME'            # HH задача "[xmlback] NEW TASK NAME"

~ » bjira create -m 'NEW TASK NAME'                         # HH задача "NEW TASK NAME"

~ » bjira create -m 'NEW TASK NAME' -d 'description'        # HH задача "NEW TASK NAME" с описанием "description"

~ » bjira create -p 12345 -s 'xmlback' -m 'NEW TASK NAME' -sp 0.5   # HH задача "[xmlback] NEW TASK NAME" на 0.5sp прилинкованная к PORTFOLIO-12345

~ » bjira create at -m 'NEW TASK NAME'                      # AT задача "[at] NEW TASK NAME"

~ » bjira create at -p 12345 -m 'NEW TASK NAME'             # AT задача "[at] NEW TASK NAME" прилинкованная к PORTFOLIO-12345

~ » bjira create at -p 'PORTFOLIO-12345' -m 'NEW TASK NAME' # AT задача "[at] NEW TASK NAME" прилинкованная к PORTFOLIO-12345

~ » bjira create bg -m 'NEW BUG NAME'                       # bug-задача "NEW TASK NAME"

~ » bjira create bug -m -s xmlback 'NEW BUG NAME'           # bug-задача "[xmlback] NEW TASK NAME"

- » bjira create release -s 'jager-experience-indexer' -v '1.0.0'   # EXP задача "jager-experience-indexer=1.0.0"

~ » bjira search --my                 # Показать последние задачи связанные со мной

~ » bjira search 15 --my              # Показать последние 15 задач связанных со мной

~ » bjira search 15 --my -t HH ARCH   # Показать последние 15 HH или ARCH задач связанных со мной

~ » bjira search 30 --my -t HH ARCH  -st Open "In Progress"   # Показать последние 15 HH или ARCH задач связанных со мной в статусах Open или "In Progress"

~ » bjira myteam             # Показать последние задачи связанные с моей командой

~ » bjira myteam 15          # Показать последние 15 задач связанных с моей командой

~ » bjira stas 11215              # Заполнить галочку про безопасность в PORTFOLIO-11215

~ » bjira stas P11215             # Заполнить галочку про безопасность в PORTFOLIO-11215

~ » bjira worth 11215 0           # Заполнить поле "Значимость изменений для пользователя" в  PORTFOLIO-11215. Второй аргумент от 0 до 3, где 0 - tax, 3 - Существенно меняет

~ » bjira view HH-12345           # Открыть задачку или портфель в дефолтном браузере

~ » bjira view                    # Открыть задачку в браузере, имя задачки взять из ветки гит-репозитория

```
