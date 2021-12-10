import pendulum
import sqlite3
import time

from pprint import pprint

import classes

def choose_mode(user):
    with sqlite3.connect('library.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM books')
        pprint(cur.fetchall())
    with sqlite3.connect('library.db') as conn:
        now = int(time.time())
        cur = conn.cursor()
        cur.execute(
            'SELECT COUNT(*) FROM orders WHERE uuid=? AND expire_date < ?',
            (user._uuid, now)
            )
        return input(f'''Автоматизированная система обслуживания читателей v1.0
        ------------
        Пользователь: {user.name or "Гость"}

        Задолженности: {cur.fetchall()[0][0]}
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


def book_order_mode(uuid):
    isbn = input('Введите ISBN книги:')
    days = 7
    with sqlite3.connect('library.db') as conn:
        cur = conn.cursor()
        cur.execute(
            'SELECT * FROM books WHERE isbn=?',
            (isbn,)
            )
        books = cur.fetchall()
        # print(books)
        if books:
            if books[0][4]:
                print('Книга уже на кого-то оформлена!')
            else:
                now = int(time.time())
                # order_time = 60 * 60 * 24 * days
                order_time = 60
                cur.execute(
                    'UPDATE books SET is_taken=1 WHERE isbn=?',
                    (isbn,)
                    )
                cur.execute(
                    'INSERT INTO orders VALUES (?, ?, ?, ?)',
                    (uuid, isbn, now, now+order_time)
                    )
                conn.commit()
                # print('Книга {} автора {} успешно оформлена на {} дней!'.format(books[0][1], books[0][2], days))
        else:
            print('Такой книги нет в БД!')


def book_return_mode(uuid):
    isbn = input('Введите ISBN книги:')
    with sqlite3.connect('library.db') as conn:
        cur = conn.cursor()
        cur.execute(
            'SELECT * FROM books WHERE isbn=?',
            (isbn,)
            )
        books = cur.fetchall()
        if books:
            cur.execute(
                'SELECT * FROM orders WHERE uuid=? AND isbn=?',
                (uuid, isbn)
                )
            orders = cur.fetchall()
            if orders:
                cur.execute(
                    'UPDATE books SET is_taken=0 WHERE isbn=?',
                    (isbn,)
                    )
                cur.execute(
                    'DELETE FROM orders WHERE uuid=? AND isbn=?',
                    (uuid, isbn)
                    )
                conn.commit()
                cur.execute(
                    'SELECT * FROM books WHERE isbn=?',
                    (isbn,)
                    )
                book = cur.fetchall()[0]
                print('Книга {} автора {} успешно возвращена!'.format(book[1], book[2]))
            else:
                print('Книга ещё не оформлена!')
        else:
            print('Такой книги нет в БД!')


def book_check_debt_mode(uuid):
    with sqlite3.connect('library.db') as conn:
        now = int(time.time())
        cur = conn.cursor()
        cur.execute(
            'SELECT * FROM orders WHERE uuid=? AND expire_date < ?',
            (uuid, now)
            )
        expired_orders = cur.fetchall()
        print('Просроченные заказы: ')
        for order in expired_orders:
            cur.execute(
                'SELECT name, author FROM orders WHERE isbn=?',
                (order[1],)
                )
            book = cur.fetchone()
            now_date = pendulum.from_timestamp(now)
            expire_date = pendulum.from_timestamp(order[3])
            diff = now_date.diff(expire_date).in_minutes()
            diff_minutes = diff % 60
            diff_hours = diff / 60 % 60
            diff_days = diff / 3600 % 24
            print('ы {} | {} {} {}'.format(
                book, diff_days, diff_hours, diff_minutes
                ))
        else:
            print('Книга не была заказана!')
