# konfig3
---
**Задание №3**
Разработать инструмент командной строки для учебного конфигурационного 
языка, синтаксис которого приведен далее. Этот инструмент преобразует текст из 
входного формата в выходной. Синтаксические ошибки выявляются с выдачей 
сообщений. 

Входной текст на учебном конфигурационном языке принимается из 
стандартного ввода. Выходной текст на языке toml попадает в файл, путь к 
которому задан ключом командной строки. 

Однострочные комментарии: 
```
:: Это однострочный комментарий 
Словари: 
{ 
} 
имя = значение; 
имя = значение; 
имя = значение; 
... 
Имена: 
[A-Z]+ 
Значения: 
• Числа. 
• Строки. 
• Словари. 
Строки: 
@"Это строка" 
Объявление константы на этапе трансляции: 
имя is значение 
Вычисление константы на этапе трансляции: 
#[имя]
```
Результатом вычисления константного выражения является значение. 
Все конструкции учебного конфигурационного языка (с учетом их 
возможной вложенности) должны быть покрыты тестами. Необходимо показать 2 
примера описания конфигураций из разных предметных областей. 
# Конвертер конфигурационного языка в TOML

Этот проект предоставляет скрипт для парсинга пользовательского конфигурационного языка и конвертации его в формат TOML. Скрипт также включает модульное тестирование для проверки работы парсера на различных конфигурациях.

## Описание

Скрипт читает входной файл с конфигурацией, состоящей из объявлений констант в виде:

```text
const имя = значение;
```

Поддерживаются следующие типы значений:
- Строки (в двойных кавычках): `"значение"`
- Целые числа: `123`
- Массивы (в круглых скобках): `("элемент1", "элемент2", ...)`

После успешного парсинга результат сохраняется в формате TOML в выходной файл.

---

## Пример конфигурации

**Входной файл (`input.txt`)**:

```text
const server_name = "my_server";
const port = 8080;
const allowed_ips = ("192.168.1.1", "192.168.1.2");
```

**Выходной файл (`output.toml`)**:

```toml
server_name = "my_server"
port = 8080
allowed_ips = ["192.168.1.1", "192.168.1.2"]
```

---

## Установка и запуск

### Требования

- Python 3.8 или выше
- Модуль `toml`

### Установка зависимостей

Установите необходимые зависимости:

```bash
pip install toml
```

### Запуск скрипта

Запустите скрипт с указанием входного и выходного файлов:

```bash
python main.py input.txt output.toml
```

### Пример вывода

Если парсинг прошёл успешно, программа выведет:

```text
Конфигурация успешно преобразована в output.toml.
```

Если в конфигурационном файле есть ошибки, программа сообщит об этом:

```text
Ошибка: Ошибка синтаксиса в строке: const name "value";
```

---

## Разбор кодов

### **1. Основной класс `ConfigParser`**

Класс `ConfigParser` отвечает за парсинг входного файла и хранение констант.

#### Разбор строки с константой
Метод `_parse_constant` ищет строки вида `const имя = значение;`:

```python
match = re.match(r'const ([a-z][a-z0-9_]*) = (.+);', line)
```
- `([a-z][a-z0-9_]*)` — имя константы, начинающееся с буквы и включающее буквы, цифры или нижние подчёркивания.
- `(.+)` — значение константы.

#### Пример:
**Вход:** `const server_name = "my_server";`  
**Выход:** ключ `'server_name'`, значение `"my_server"`.

---

### **2. Разбор значений**

Метод `_parse_value` определяет тип значения:
- **Строка:** если значение заключено в кавычки `"..."`.
- **Число:** если значение — целое число.
- **Массив:** если значение обёрнуто в скобки `(...)`.

**Пример парсинга:**

```python
if value.startswith('"') and value.endswith('"'):
    return value[1:-1]  # Возвращает строку без кавычек
elif re.match(r'^\d+$', value):
    return int(value)  # Преобразует в целое число
elif value.startswith('(') and value.endswith(')'):
    return self._parse_array(value[1:-1])
```

---

### **3. Обработка массивов**

Метод `_parse_array` разбивает строку массива на элементы и вызывает `_parse_value` для каждого элемента.

```python
items = [self._parse_value(item.strip()) for item in value.split(',')]
```

**Пример:**

**Вход:** `("192.168.1.1", "192.168.1.2")`  
**Выход:** `["192.168.1.1", "192.168.1.2"]`.

---

### **4. Обработка выражений `.()`**

Метод `_parse_constant_expression` обрабатывает конструкции вида `.(`имя`).`, которые ссылаются на ранее объявленные константы:

```python
match = re.match(r'\.\((.+?)\)\.', line)
if name not in self.constants:
    raise NameError(f"Константа '{name}' не объявлена.")
```

**Пример:**
- Если `const port = 8080;` уже объявлено, то строка `. (port).` вернёт `8080`.

---

### **5. Основной метод `parse`**

Метод `parse` обрабатывает все строки файла, определяя их тип и вызывая нужные функции:

```python
if line.startswith("const"):
    self._parse_constant(line)
elif line.startswith(".(") and line.endswith(")."):
    self._parse_constant_expression(line)
else:
    raise SyntaxError(f"Неизвестная конструкция: {line}")
```

---

## Тестирование

Проект включает модульные тесты для проверки функциональности парсера. Тесты находятся в файле `test_config_parser.py`.

Для запуска тестов используйте:

```bash
python -m unittest test_config_parser.py
```

### Покрываемые сценарии

- Парсинг корректных конфигураций (веб-сервер, база данных, приложение)
- Обработка ошибок синтаксиса
- Обработка неопределённых констант
- Обработка некорректных значений

---

## Примеры конфигураций

### Конфигурация веб-сервера

```text
const server_name = "my_server";
const port = 8080;
const allowed_ips = ("192.168.1.1", "192.168.1.2");
```

### Конфигурация базы данных

```text
const db_name = "my_database";
const db_user = "admin";
const db_password = "secret";
const db_hosts = ("localhost", "192.168.1.10");
```

### Конфигурация приложения

```text
const app_name = "MyApp";
const version = "1.0.0";
const features = ("feature1", "feature2", "feature3");
```

---

## Структура проекта

```plaintext
├── main.py                # Основной скрипт
├── config_parser.py       # Класс парсера конфигурации
├── test_config_parser.py  # Модульные тесты
└── README.md              # Документация
```

---

## Лицензия

Этот проект распространяется под лицензией **MIT**.
