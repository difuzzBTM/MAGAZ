# register_handler.py
from flask import Flask, render_template, request, redirect, url_for, flash
from forms import RegisterForm
from db_session import create_session
from __all_models import Person
import hashlib
import re


def hash_password(password):
    """Хеширование пароля"""
    return hashlib.sha256(password.encode()).hexdigest()


def validate_register_data(name, email, password, confirm_password):
    """Валидация данных регистрации"""
    errors = []

    if not name or len(name) < 2:
        errors.append("Имя должно содержать минимум 2 символа")

    # Простая валидация email
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        errors.append("Введите корректный email адрес")

    if len(password) < 6:
        errors.append("Пароль должен содержать минимум 6 символов")

    if password != confirm_password:
        errors.append("Пароли не совпадают")

    return errors


def register_user(name, surname, email, password, login, address=None):
    """
    Регистрация нового пользователя
    """
    session = create_session()

    try:
        # Проверка на существующего пользователя с таким email
        existing_user_email = session.query(Person).filter(Person.email == email).first()
        if existing_user_email:
            return False, "Пользователь с таким email уже существует"

        # Проверка на существующего пользователя с таким login
        existing_user_login = session.query(Person).filter(Person.login == login).first()
        if existing_user_login:
            return False, "Пользователь с таким логином уже существует"

        # Создание нового пользователя
        new_person = Person()
        new_person.name = name
        new_person.surname = surname
        new_person.email = email
        new_person.login = login
        new_person.password = hash_password(password)

        if address:
            new_person.address = address

        session.add(new_person)
        session.commit()

        return True, "Регистрация успешно завершена"

    except Exception as e:
        session.rollback()
        return False, f"Ошибка при регистрации: {str(e)}"
    finally:
        session.close()


# Добавляем обработчики маршрутов в app.py
def setup_register_routes(app):
    """Настройка маршрутов для регистрации"""

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegisterForm()

        if request.method == 'POST' and form.validate_on_submit():
            name = form.name.data
            email = form.email.data
            password = form.password.data
            confirm_password = form.confirm_password.data

            # Создаем логин из email (часть до @)
            login = email.split('@')[0]
            surname = ""  # По умолчанию пустая фамилия

            # Проверка данных
            errors = validate_register_data(name, email, password, confirm_password)

            if errors:
                for error in errors:
                    flash(error, 'error')
                return render_template('register.html', form=form)

            # Регистрация пользователя
            success, message = register_user(
                name=name,
                surname=surname,
                email=email,
                password=password,
                login=login
            )

            if success:
                flash(message, 'success')
                return redirect(url_for('login'))
            else:
                flash(message, 'error')
                return render_template('register.html', form=form)

        return render_template('register.html', form=form)

# В app.py добавить после создания app:
# from register_handler import setup_register_routes
# setup_register_routes(app)