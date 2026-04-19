from flask import Flask, render_template, request, redirect, session, url_for
from forms import (LoginForm, RegisterForm, ResetPasswordForm,
                  ProductFilterForm, AddToCartForm, CheckoutForm,
                  ProfileEditForm, ChangePasswordForm)
from data.db_session import global_init, create_session
from data.__all_models import Person
from data.__all_models import Product, ProductType, Size, ProductSize
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key123'

global_init('db/shop.db')


@app.route('/')
@app.route('/main')
def main():
    db_sess = create_session()

    categories = db_sess.query(ProductType).all()
    sizes = db_sess.query(Size).all()

    form = ProductFilterForm()
    form.category.choices = [('', 'Все категории')] + [(str(c.id), c.name) for c in categories]
    form.size.choices = [('', 'Все размеры')] + [(str(s.id), s.name) for s in sizes]

    search_query = request.args.get('search', '')
    category_id = request.args.get('category', '')
    size_id = request.args.get('size', '')
    price_min = request.args.get('price_min', type=float)
    price_max = request.args.get('price_max', type=float)
    sort = request.args.get('sort', 'name_asc')

    form.search.data = search_query
    if category_id:
        form.category.data = category_id
    if size_id:
        form.size.data = size_id
    form.price_min.data = price_min
    form.price_max.data = price_max
    form.sort.data = sort

    query = db_sess.query(Product).join(ProductType).outerjoin(ProductSize).outerjoin(Size)

    if search_query:
        query = query.filter(Product.name.ilike(f'%{search_query}%'))
    if category_id:
        query = query.filter(Product.type_id == int(category_id))
    if size_id:
        query = query.filter(ProductSize.size_id == int(size_id))
    if price_min is not None:
        query = query.filter(Product.cost >= price_min)
    if price_max is not None:
        query = query.filter(Product.cost <= price_max)

    if sort == 'name_asc':
        query = query.order_by(Product.name.asc())
    elif sort == 'name_desc':
        query = query.order_by(Product.name.desc())
    elif sort == 'price_asc':
        query = query.order_by(Product.cost.asc())
    elif sort == 'price_desc':
        query = query.order_by(Product.cost.desc())

    products = query.all()

    return render_template('main_page.html', form=form, products=products)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.confirm_password.data:
            return render_template('register.html', form=form,
                                   message="Пароли не совпадают")

        db_sess = create_session()
        existing_user = db_sess.query(Person).filter(Person.email == form.email.data).first()
        if existing_user:
            return render_template('register.html', form=form,
                                   message="Пользователь с таким email уже существует")

        person = Person(
            surname=form.name.data,
            name=form.name.data,
            login=form.email.data,
            email=form.email.data
        )
        person.set_password(form.password.data)

        db_sess.add(person)
        db_sess.commit()

        return redirect('/login')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        db_sess = create_session()
        person = db_sess.query(Person).filter(Person.email == email).first()

        if not person:
            return render_template('login.html', form=form, message="Пользователь не найден")

        if not person.check_password(password):
            return render_template('login.html', form=form, message="Неверный пароль")

        session['user_id'] = person.id
        return redirect('/profile')

    return render_template('login.html', form=form)


@app.route('/reset', methods=['GET', 'POST'])
def reset():
    form = ResetPasswordForm()
    if request.method == 'POST':
        email = request.form['email']
        new_password = request.form.get('new_password')
        new_password_again = request.form.get('new_password_again')

        return render_template('reset.html', form=form,
                               message="Инструкции по сбросу отправлены на почту (заглушка)")

    return render_template('reset.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('main'))

@app.route('/prod/<int:id>')
def prod(id):
    db_sess = create_session()
    product = db_sess.query(Product).get(id)
    if not product:
        return "Товар не найден", 404
    form = AddToCartForm()
    return render_template('prod_page.html', product=product, form=form)


@app.route('/profile')
def profile():
    form = ProfileEditForm()
    password_form = ChangePasswordForm()
    return render_template('profile.html', form=form, password_form=password_form)


@app.route('/cart')
def cart():
    checkout_form = CheckoutForm()
    return render_template('cart.html', form=checkout_form)


@app.route('/payout')
def payout():
    checkout_form = CheckoutForm()
    return render_template('payout.html', form=checkout_form)


@app.route('/order_status')
def order_status():
    return render_template('order_status.html')


if __name__ == '__main__':
    app.run(debug=True, port=8010)