# Лабораторная работа №3

Вариант №2621: Twitter/X.

В этой реализации лабораторной используется Python-стек: `pytest + selenium`.

## Содержимое каталога

- `docs/use-cases.md` — набор прецедентов использования.
- `docs/test-coverage.md` — матрица покрытия и список тест-кейсов.
- `tests/test_x_public_flows.py` — автоматизированные UI-тесты на Python.
- `conftest.py` — Selenium fixtures и выбор браузера.
- `results/chrome-2026-03-18.md` — результаты контрольного прогона в Chrome от `2026-03-18`.

## Ограничения сценариев

- Покрываются только публичные сценарии без авторизации.
- Не включены вход через Google/Apple, публикация постов, работа с SMS и действия после логина.
- Для открытия полной формы регистрации используется путь `landing page -> Create account`.
- Все локаторы построены на XPath по видимому тексту и семантическим атрибутам, без `id`.

## Установка

```bash
cd lab3
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Запуск

Chrome headless:

```bash
cd lab3
source .venv/bin/activate
pytest -q --browser chrome
```

Firefox headless:

```bash
cd lab3
source .venv/bin/activate
pytest -q --browser firefox
```

Запуск с видимым окном браузера:

```bash
pytest -q --browser chrome --headed
```

## Что проверяют тесты

- Загрузка публичной landing page и отображение onboarding-элементов.
- Скрытие cookie banner.
- Доступность формы входа.
- Переход к восстановлению пароля.
- Открытие формы регистрации и переключение поля `Phone -> Email`.

