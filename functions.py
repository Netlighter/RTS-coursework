import sqlite3

import classes

def choose_mode(user):
    return input(f'''Автоматизированная система обслуживания читателей v1.0
    ------------
    Пользователь: {user.name or "Гость"}

    Задолженности:
    ------------
    Выберите действие:
    1. авторизовать читательский билет
    2. оформить книгу
    3. вернуть книгу
    4. проверить задолженности

    q. выйти

    >>>''')


def auth_mode():
    uuid = input('Введите UUID участника клуба: ')
    with sqlite3.connect('library.db') as conn:
        cur = conn.cursor()
        cur.execute(
            'SELECT * FROM users WHERE uuid=?',
            (uuid,)
            )
        user = cur.fetchall()
        if user:
            
            return classes.User(*user[0])
        else:
            return None
