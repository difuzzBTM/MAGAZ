# register_utils.py
import re


def validate_email(email):
    """Валидация email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def generate_login_from_email(email):
    """Генерация логина из email"""
    return email.split('@')[0]


def validate_password_strength(password):
    """Проверка сложности пароля"""
    errors = []

    if len(password) < 6:
        errors.append("Пароль должен быть не менее 6 символов")

    if not any(c.isupper() for c in password):
        errors.append("Пароль должен содержать хотя бы одну заглавную букву")

    if not any(c.islower() for c in password):
        errors.append("Пароль должен содержать хотя бы одну строчную букву")

    if not any(c.isdigit() for c in password):
        errors.append("Пароль должен содержать хотя бы одну цифру")

    return errors