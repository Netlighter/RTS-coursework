SEPARATOR = '------------'
GUEST = 'Гость'

SUCCESS_AUTH = '-\nУспешный вход под именем {}!\n-'
SUCCESS_ORDER = 'Книга "{}" автора {} успешно оформлена на {} дней!'
SUCCESS_RETURN = 'Книга "{}" автора {} успешно возвращена!'

FAIL_ALREADY_AUTHORIZED = '-\nВы уже авторизованы под именем {}!\n-'
FAIL_ALREADY_ORDERED = 'Книга уже на кого-то оформлена!'
FAIL_ORDER_NO_BOOKS = 'Все книги разобраны!'
FAIL_ORDER_NOT_ORDERED_YET = 'Книга ещё не оформлена!'
FAIL_ORDER_NOT_IN_DB = 'Такой книги нет в БД!'

EXCEPTION_DIFF_TYPE_ERROR = 'Невозможно разделить разницу времени: передан неправильный тип'

INFO_AUTH_MODE = '-\nРежим авторизации...\n-'
INFO_WELCOME = '{0}\nАвтоматизированная Система Обслуживания Читателей v1.0\n{0}'.format(SEPARATOR)

INPUT_UUID = 'Введите UUID участника клуба: '
INPUT_ISBN_CHOOSE = '1. Отсканировать ISBN\n2. Ввести ISBN вручную\n>>> '
INPUT_ISBN = 'Введите ISBN книги:'

GREETING_USER = 'Пользователь:'
GREETING_DEBTS = 'Задолженности:'
GREETING_SELECT_ACTION = 'Выберите действие:'
GREETING_ACTIONS = [
    'авторизовать читательский билет',
    'оформить книгу',
    'вернуть книгу',
    'проверить задолженности'
    ]
GREETING_EXIT_TITLE = 'выйти'

CHECK_DEBT_EXPIRED = '{}, автор: {}. Срок: {} дн. {} ч. {} мин.'
CHECK_DEBT_NON_EXPIRED = '{}, автор: {}. До конца срока: {} дн. {} ч. {} мин.'

ORDERS_EXPIRED = 'Просроченные заказы:'
ORDERS_NON_EXPIRED = 'Не просроченные заказы:'
