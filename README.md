
# bjira - работаем с jira из консоли

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

Для доступа можно также использовать [токен](https://confluence.atlassian.com/enterprise/using-personal-access-tokens-1026032365.html)

```shell script
bjira settoken
```

Пароль и токен не хранятся одновременно — задание токена сбрасывает пароль и наоборот

### Использовать

```shell script
~ » bjira create -s 'xmlback' -m 'NEW TASK NAME'            # HH задача "[xmlback] NEW TASK NAME"

~ » bjira create -m 'NEW TASK NAME'                         # HH задача "NEW TASK NAME"

~ » bjira create -m 'NEW TASK NAME' -d 'description'        # HH задача "NEW TASK NAME" с описанием "description"

~ » bjira create -m 'NEW TASK NAME' -d 'description' -l 'label-1, label-2'        # HH задача "NEW TASK NAME" с описанием "description" и тэгами "label-1, label-2"

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

~ » bjira search 25 -t HH -st '!closed' '!released' '!Deployed' -m assignee # Показать последние 25 HH задач назначенных на меня в статусах не closed, released, Deployed

~ » bjira search -m -t PORTFOLIO -st 'y' # поискать задачи у которых статус маппится в ✅ (y, v, Y, V)
~ » bjira search -m -t PORTFOLIO -st '!y' # поискать задачи у которых статус маппится не в ✅ (y, v, Y, V)

~ » bjira search -dt sloniki      # Искать задачи для Dev Team "sloniki"

~ » bjira stas 11215              # Заполнить галочку про безопасность в PORTFOLIO-11215

~ » bjira stas P11215             # Заполнить галочку про безопасность в PORTFOLIO-11215

~ » bjira worth 11215 0           # Заполнить поле "Значимость изменений для пользователя" в  PORTFOLIO-11215. Второй аргумент от 0 до 3, где 0 - tax, 3 - Существенно меняет

~ » bjira view HH-12345           # Открыть задачку или портфель в дефолтном браузере

~ » bjira view                    # Открыть задачку в браузере, имя задачки взять из ветки гит-репозитория

```

### Project-ops commands (fork extension)

```shell script
~ » bjira edit PORTFOLIO-53307 --due 2026-05-15                         # set Due Date
~ » bjira edit PORTFOLIO-53307 --description-file ./spec.md --force     # overwrite description from file
~ » bjira edit PORTFOLIO-53307 --label urgent --label q2-2026           # merge labels with existing
~ » bjira edit PORTFOLIO-53307 --labels-clear                           # remove all labels
~ » bjira edit PORTFOLIO-53307 --assignee i.moltyaninov                 # reassign
~ » bjira edit PORTFOLIO-53307 --assignee none                          # unassign

~ » bjira comment PORTFOLIO-53307 "готово, ждём ревью"                  # add comment
~ » bjira comment PORTFOLIO-53307 --from-file ./update.md               # add comment from file

~ » bjira comments PORTFOLIO-53307                                      # list last 5 comments
~ » bjira comments PORTFOLIO-53307 -n 20                                # list last 20

~ » bjira status PORTFOLIO-53307 "Development: In progress"             # transition (fuzzy match)
~ » bjira status PORTFOLIO-53307 1501                                   # transition by id

~ » bjira link PORTFOLIO-53307 Blocks PORTFOLIO-54000                   # link existing issues
```

**Exit codes:** `0` success, `2` arg error, `3` API error (auth/permission/not-found, ambiguous/unknown match). Pass `-v` for SDK debug logging.

**Safety:** `--force` is required for `edit --description` and `edit --summary` when the existing value is non-empty. All other operations are additive or trivially reversible via Jira history.
