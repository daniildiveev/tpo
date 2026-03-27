# Тестовое Покрытие

## Матрица покрытия

| Use case | Покрывающие тесты |
| --- | --- |
| UC-01. Просмотр публичной landing page | TC-01 |
| UC-02. Управление cookie banner | TC-02 |
| UC-03. Открытие формы входа | TC-03 |
| UC-04. Переход к восстановлению пароля | TC-04 |
| UC-05. Открытие формы регистрации | TC-05 |
| UC-06. Переключение канала регистрации с телефона на email | TC-05 |

## Набор тест-кейсов

| ID | Название | Основание | Приоритет | Автоматизация | Ожидаемый результат |
| --- | --- | --- | --- | --- | --- |
| TC-01 | Отображение landing page для гостя | UC-01 | High | Python Selenium | Видны `Happening now`, `Create account`, `Sign in`, ссылки на правовые документы |
| TC-02 | Скрытие cookie banner | UC-02 | High | Python Selenium | После нажатия `Refuse non-essential cookies` баннер исчезает |
| TC-03 | Отображение формы входа | UC-03 | High | Python Selenium | Видны `Sign in to X`, поле username, кнопки `Next`, `Forgot password?`, `Sign up` |
| TC-04 | Переход к password reset flow | UC-04 | Medium | Python Selenium | После `Forgot password?` открывается экран `Find your X account` |
| TC-05 | Открытие формы регистрации и переключение на email | UC-05, UC-06 | High | Python Selenium | После `Create account` открывается форма `Create your account`; `Use email instead` заменяет `Phone` на `Email` |
