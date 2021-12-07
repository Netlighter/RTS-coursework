'''
Функция считывания читательского билета
Функция оформления книги на читательский билет
Функция возврата книги по читательскому билету
Функция уведомления держателя читательского билета о сроке сдачи литературы
'''

import sys

import classes
import functions

user = classes.User(None, None)

while True:
    prompt = functions.choose_mode(user)
    
    if prompt == 'q':
        sys.exit()

    if prompt == '1':
        if user.name:
            print('Вы уже авторизованы под именем {}!'.format(user.name))
        else:
            print('Режим авторизации...')
            user = functions.auth_mode()
            print('Успешный вход под именем {}!'.format(user.name))

    if prompt == '2':
        break

    if prompt == '3':
        break

    if prompt == '4':
        break
    
    
