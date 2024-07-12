LEXICON_RU: dict[str, str] = {
    '/start': '<b>Хей!</b> Давай проверю, есть ли у тебя доступ.\n'
              'Кликай по меню или напиши <b>"каталог"</b> ',
    '/help': 'Всё очень просто, если ты <b>сотрудник</b>, то есть доступ.\n'
             'Жми на каталог или пиши в сообщениях модель, для <b>поиска</b>.\n'
             'Бот не сложный, разберёшся',
    'choice_user': 'Выбери пользователя из списка:',
    'input_name': 'Введи имя сотрудника',
    'input_surname': 'Введи фамилию сотрудника',
    'input_phone_number': 'Введи номер телефона в таком формате <b>+7 701 123 4567</b>',
    'username': '<b>Никнейм телеграмма: </b>',
    'tg_id': '<b>Телеграмм ID: </b>',
    'employee_name': '<b>Пользователь</b>: ',
    'role': '<b>Статус</b>: ',
    'phone_number': '<b>Номер телефона</b>: ',
    'success': 'Данные успешно изменены!',
    'update_role': 'Обновить роль',
    'product_name': '<b>Наименование: </b>',
    'category': '<b>Категория: </b>',
    'balance': '<b>Баланс: </b>',
    'purchase_price': '<b>Закупочная: </b>',
    'cash_price': '<b>Наличными: </b>',
    'credit_price': '<b>Кредит: </b>',
    'not_access': 'Ой! Доступа, нет. Пиши <b>аднмину</b>.',
    'setting': 'Доступные опции: ',
    'catalog': 'Выбери категорию товара: ',
    'category_list': 'Список товаров в категории ',
    'search_reply': 'Вот что удалось найти: '
}

LEXICON_BUTTON: dict[str, str] = {
    'main': 'Главная',
    'catalog': 'Каталог',
    'example': 'Пример для поиска: вытяжка midea',
    'change_dt': 'Изменить данные',
    'account': 'Моя анкета',
    'employee_list': 'Список сотрудников',
    'set_employee': 'Назначить сотрудника',
    'guests_list': 'Список гостей',
    'delete_employee': 'Удалить сотрудника'
}

LEXICON_CALLBACK: dict[str, str] = {
    'role': 'role_',
    'update_employee': 'update-employee_',
    'set_employee': 'set-employee_',
    'employees_list': 'list_employee',
    'employee': 'employee_',
    'user': 'user_',
    'users_list': 'list_users',
    'guests': 'guests',
    'category': 'category_',
    'product': 'product_',
    'delete_employee': 'delete-employee_'
}
