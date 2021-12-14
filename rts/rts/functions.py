import pendulum
import sqlite3
import time

from random import choice
from pprint import pprint

import classes
import exceptions
import strings


def split_diff(diff):
    if isinstance(diff, int):
        return (diff // 1440, diff // 60 % 24, diff % 60)
    else:
        raise exceptions.DiffTypeError(strings.EXCEPTION_DIFF_TYPE_ERROR)


def greet(user, debt_num):
    action_message = (
        strings.GREETING_SELECT_ACTION,
        '\n'.join('{}. {}'.format(k, v) for k, v in enumerate(strings.GREETING_ACTIONS, 1))
        )
    message_order = (
        strings.INFO_WELCOME,
        strings.GREETING_USER,
        user.name,
        strings.GREETING_DEBTS,
        debt_num,
        strings.SEPARATOR,
        *action_message,
        strings.GREETING_EXIT_TITLE
        )
    return '{}\n{} {}\n{} {}\n{}\n{}\n\n{}\n\n>>>'.format(*message_order)


def choose_mode(user):
    with sqlite3.connect('library.db') as conn:
        now = int(pendulum.now().format('X'))
        cur = conn.cursor()
        cur.execute(
            'SELECT COUNT(*) FROM orders WHERE uuid=? AND expire_date < ?',
            (user._uuid, now)
            )
        username = user.name or 'Гость'
        debt_num = cur.fetchall()[0][0]
        return input(greet(username, debt_num))


def auth_mode():
    uuid = input(strings.INPUT_UUID)
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


def scan_isbn_auto(ordered_only):
    with sqlite3.connect('library.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT isbn FROM books')
        all_books = [book[0] for book in cur.fetchall()]
        cur.execute('SELECT isbn FROM orders')
        ordered_books = [book[0] for book in cur.fetchall()]
        if ordered_only:
            try:
                return choice(ordered_books)
            except IndexError:
                return None
        else:
            try:
                return choice(list(set(all_books) - set(ordered_books)))
            except IndexError:
                return None


def scan_isbn(ordered_only):
    prompt = input(strings.INPUT_ISBN_CHOOSE)
    if prompt == '1':
        return scan_isbn_auto(ordered_only)
    if prompt == '2':
        return input(strings.INPUT_ISBN)


def book_order_mode(uuid):
    isbn = scan_isbn(False)
    days = 7
    with sqlite3.connect('library.db') as conn:
        cur = conn.cursor()
        cur.execute(
            'SELECT * FROM books WHERE isbn=?',
            (isbn,)
            )
        books = cur.fetchall()
        if books:
            if books[0][4]:
                print(strings.already_ordered)
            else:
                now = int(pendulum.now().format('X'))
                order_time = 60 * 60 * 24 * days
                cur.execute(
                    'UPDATE books SET is_taken=1 WHERE isbn=?',
                    (isbn,)
                    )
                cur.execute(
                    'INSERT INTO orders VALUES (?, ?, ?, ?)',
                    (uuid, isbn, now, now+order_time)
                    )
                conn.commit()
                print(strings.SUCCESS_ORDER.format(*books[0], days))
        else:
            print(strings.FAIL_ORDER_NO_BOOKS)


def book_return_mode(uuid):
    isbn = scan_isbn(True)
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
                print(strings.success_return.format(*book))
            else:
                print(strings.FAIL_ORDER_NOT_ORDERED_YET)
        else:
            print(strings.FAIL_ORDER_NOT_IN_DB)


def book_check_debt_mode(uuid):
    with sqlite3.connect('library.db') as conn:
        now = int(pendulum.now().format('X'))
        cur = conn.cursor()
        cur.execute(
            'SELECT * FROM orders WHERE uuid=? AND expire_date < ?',
            (uuid, now)
            )
        expired_orders = cur.fetchall()
        print('\n{} '.format(strings.ORDERS_EXPIRED))
        for order in expired_orders:
            cur.execute(
                'SELECT name, author FROM books WHERE isbn=?',
                (order[1],)
                )
            book = cur.fetchone()
            book_title, book_author = book
            now_date = pendulum.from_timestamp(now)
            expire_date = pendulum.from_timestamp(order[3])
            diff = now_date.diff(expire_date).in_minutes()
            diff_days, diff_hours, diff_minutes = split_diff(diff)
            print(strings.CHECK_DEBT_EXPIRED.format(
                book_title, book_author, diff_days, diff_hours, diff_minutes
                ))

        cur.execute(
            'SELECT * FROM orders WHERE uuid=? AND expire_date > ?',
            (uuid, now)
            )
        non_expired_orders = cur.fetchall()
        print('\n{} '.format(strings.ORDERS_NON_EXPIRED))
        for order in non_expired_orders:
            cur.execute(
                'SELECT name, author FROM books WHERE isbn=?',
                (order[1],)
                )
            book = cur.fetchone()
            book_title, book_author = book
            now_date = pendulum.from_timestamp(now)
            expire_date = pendulum.from_timestamp(order[3])
            diff = expire_date.diff(now_date).in_minutes()
            diff_days, diff_hours, diff_minutes = split_diff(diff)
            print(strings.CHECK_DEBT_NON_EXPIRED.format(
                book_title, book_author, diff_days, diff_hours, diff_minutes
                ))
