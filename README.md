# Менеджер задач

## Описание
Это приложение для управления задачами, позволяющее регистрировать задачи от клиента, назначать руководителей и исполнителей, устанавливать даты начала и дедлайны, а также отмечать завершенные задачи.

## Функционал
1. **Регистрация задач**: Задачи регистрируются с указанием клиента и описания.
2. **Назначение задач**: Руководитель назначает исполнителя, устанавливает дату начала и дедлайн.
3. **Обновление задач**: Задачи могут быть обновлены с изменением исполнителя и дат.
4. **Завершение задач**: Исполнители могут завершать задачи, и фиксируется дата и время завершения.
5. **Просмотр задач исполнителя**: Возможность просмотра всех задач конкретного исполнителя.


## Структура проекта
task-manager/
├── database.py # Модуль для работы с базой данных SQLite
├── main.py # Главный файл для запуска приложения
├── task_manager.kv # Файл разметки Kivy для пользовательского интерфейса
├── task.bd # Файл базы данных SQLite
└── README.md # Файл с описанием проекта

## Использование
1. Запустите приложение:
    ```bash
    python main.py
    ```
2. Интерфейс приложения включает следующие экраны:
    - **Главный экран**: Позволяет перейти к добавлению задачи, обновлению задачи, завершению задачи и просмотру задач исполнителя.
    - **Добавить задачу**: Введите имя клиента и описание задачи, затем нажмите "Добавить задачу".
    - **Назначить задачу**: Введите ID задачи, имя руководителя, имя исполнителя, дату начала и дедлайн, затем нажмите "Назначить задачу".
    - **Обновить задачу**: Введите ID задачи, имя руководителя, имя исполнителя, дату начала и дедлайн, затем нажмите "Обновить задачу".
    - **Завершить задачу**: Введите ID задачи и нажмите "Завершить задачу".
    - **Задачи исполнителя**: Введите имя исполнителя и ID задачи, чтобы завершить задачу.


## Объяснение кода

### main.py
Этот файл отвечает за основную логику приложения и использует KivyMD для создания интерфейса.

- `MainScreen`: Главный экран с кнопками для перехода на другие экраны.
- `AddTaskScreen`: Экран для добавления новой задачи. Проверяет корректность ввода и сохраняет задачу в базу данных.
- `AssignTaskScreen`: Экран для назначения задачи. Позволяет установить руководителя, исполнителя, дату начала и дедлайн.
- `UpdateTaskScreen`: Экран для обновления задачи. Проверяет корректность введенных данных и обновляет информацию о задаче.
- `CompleteTaskScreen`: Экран для завершения задачи. Обновляет статус задачи и фиксирует дату завершения.
- `ExecutorTaskScreen`: Экран для завершения задачи исполнителем и просмотра оставшихся задач.

### task_manager.kv
Этот файл определяет разметку пользовательского интерфейса, включая элементы управления и их расположение на экране.

### database.py
Этот файл содержит класс `Database`, который взаимодействует с базой данных SQLite для хранения и управления задачами.

- `create_table()`: Создает таблицу задач, если она еще не существует.
- `add_task(client, description)`: Добавляет новую задачу.
- `update_task(task_id, manager, executor, start_date, deadline)`: Обновляет информацию о задаче.
- `complete_task(task_id)`: Обновляет статус задачи на "completed" и фиксирует дату и время завершения.
- `get_tasks_by_executor(executor)`: Возвращает все незавершенные задачи для указанного исполнителя.
- `is_task_completed(task_id)`: Проверяет, завершена ли задача, и возвращает дату завершения, если она завершена.


## Автор
Николау Виолетта


