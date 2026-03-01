from flask import Flask, render_template, request
from forms import (LoginForm, RegisterForm, ResetPasswordForm,
                  ProductFilterForm, AddToCartForm, CheckoutForm,
                  ProfileEditForm, ChangePasswordForm)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey-for-wtf-forms-2026'  # обязательный ключ для CSRF-защиты

#Маршруты для всех страниц

@app.route('/')
@app.route('/main')
def main():
    product_filter_form = ProductFilterForm()
    return render_template('main_page.html', form=product_filter_form)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', form=form)

@app.route('/register')
def register():
    form = RegisterForm()
    return render_template('register.html', form=form)

@app.route('/reset')
def reset():
    form = ResetPasswordForm()
    return render_template('reset.html', form=form)

@app.route('/prod')
def prod():
    add_to_cart_form = AddToCartForm()
    return render_template('prod_page.html', form=add_to_cart_form)

@app.route('/profile')
def profile():
    profile_form = ProfileEditForm()
    password_form = ChangePasswordForm()
    return render_template('profile.html', profile_form=profile_form, password_form=password_form)

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/payout')
def payout():
    checkout_form = CheckoutForm()
    return render_template('payout.html', form=checkout_form)

@app.route('/order_status')
def order_status():
    return render_template('order_status.html')

if __name__ == '__main__':
    app.run(debug=True, port=8010)