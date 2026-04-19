from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, IntegerField, FloatField, TextAreaField, \
    RadioField, SelectField, FileField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, Optional


#пользователь

class LoginForm(FlaskForm):
    email = EmailField('Email',
                       validators=[DataRequired(message='Email обязателен'), Email(message='Некорректный email')])
    password = PasswordField('Пароль', validators=[DataRequired(message='Введите пароль')])
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired(message='Имя обязательно'), Length(min=2, max=20)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(),
                                                   Length(min=6, message='Пароль должен быть минимум 6 символов')])
    confirm_password = PasswordField('Подтвердите пароль',
                                     validators=[DataRequired(), EqualTo('password', message='Пароли не совпадают')])
    submit = SubmitField('Зарегистрироваться')


class ResetPasswordForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Отправить ссылку для сброса')



class ProductFilterForm(FlaskForm):
    search = StringField('Поиск', validators=[Optional()])
    category = SelectField('Категория', choices=[('', 'Все категории')], validators=[Optional()])
    size = SelectField('Размер', choices=[('', 'Все размеры')], validators=[Optional()])
    price_min = FloatField('Цена от', validators=[Optional(), NumberRange(min=0)])
    price_max = FloatField('Цена до', validators=[Optional(), NumberRange(min=0)])
    sort = SelectField('Сортировка', choices=[
        ('name_asc', 'Название (А-Я)'),
        ('name_desc', 'Название (Я-А)'),
        ('price_asc', 'Цена (по возрастанию)'),
        ('price_desc', 'Цена (по убыванию)'),
    ], validators=[Optional()])
    submit = SubmitField('Применить')


class AddToCartForm(FlaskForm):
    quantity = IntegerField('Количество', validators=[DataRequired(), NumberRange(min=1, max=99)], default=1)
    submit = SubmitField('Добавить в корзину')



class CheckoutForm(FlaskForm):
    first_name = StringField('Имя', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Фамилия', validators=[DataRequired(), Length(min=2, max=30)])
    address = StringField('Адрес доставки', validators=[DataRequired(), Length(min=5, max=50)])
    phone = StringField('Телефон', validators=[DataRequired(), Length(min=10, max=15)])

    payment_method = RadioField('Способ оплаты',
                                choices=[('card', 'Банковская карта'),
                                         ('cash', 'Наличные при получении')],
                                validators=[DataRequired()])

    comment = TextAreaField('Комментарий к заказу', validators=[Optional(), Length(max=500)])

    submit = SubmitField('Оплатить')


#профиль

class ProfileEditForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired(), Length(min=2, max=50)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Телефон', validators=[Optional(), Length(min=10, max=15)])
    avatar = FileField('Аватар', validators=[Optional()])  # для загрузки изображения
    submit = SubmitField('Сохранить изменения')


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Текущий пароль', validators=[DataRequired()])
    new_password = PasswordField('Новый пароль', validators=[DataRequired(), Length(min=6)])
    confirm_new_password = PasswordField('Подтвердите новый пароль',
                                         validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Изменить пароль')