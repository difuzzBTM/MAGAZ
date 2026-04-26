from flask import Flask, render_template, request, redirect, session, url_for
from forms import (LoginForm, RegisterForm, ResetPasswordForm,
                  ProductFilterForm, AddToCartForm, CheckoutForm,
                  ProfileEditForm, ChangePasswordForm)
from data.db_session import global_init, create_session
from data.__all_models import  ProductType, ProductSize, Person, Product, Size, Cart, Order, PaymentType, OrderType, OrderItem, UserPaymentMethod, UserAddress
from flask import flash

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


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db_sess = create_session()
    person = db_sess.query(Person).get(session['user_id'])


    profile_form = ProfileEditForm(obj=person)
    password_form = ChangePasswordForm()

    #Сохранить настройки
    if request.method == 'POST' and 'save_settings' in request.form:
        person.newsletter = 'newsletter' in request.form
        person.save_history = 'save_history' in request.form
        db_sess.commit()
        flash('Настройки сохранены')
        return redirect(url_for('profile'))

    #текущие заказы
    current_orders = db_sess.query(Order).filter(
        Order.person_id == person.id,
        Order.order_type_rel.has(OrderType.name != 'Доставлен')
    ).all()

    addresses = person.addresses
    payment_methods = person.payment_methods

    return render_template(
        'profile.html',
        person=person,
        form=profile_form,
        password_form=password_form,
        current_orders=current_orders,
        addresses=addresses,
        payment_methods=payment_methods
    )


@app.route('/profile/add_address', methods=['POST'])
def add_address():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    db_sess = create_session()
    new_address = request.form.get('address', '').strip()
    if new_address:
        addr = UserAddress(
            person_id=session['user_id'],
            address=new_address,
            is_default=False
        )
        db_sess.add(addr)
        db_sess.commit()
    return redirect(url_for('profile'))


@app.route('/profile/delete_address/<int:addr_id>')
def delete_address(addr_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    db_sess = create_session()
    addr = db_sess.query(UserAddress).filter(
        UserAddress.id == addr_id,
        UserAddress.person_id == session['user_id']
    ).first()
    if addr:
        db_sess.delete(addr)
        db_sess.commit()
    return redirect(url_for('profile'))


@app.route('/profile/add_card', methods=['POST'])
def add_card():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    db_sess = create_session()
    card_number = request.form.get('card_number', '').strip()
    card_type = request.form.get('card_type', '').strip()
    if card_number:
        masked = card_number[:4] + ' **** **** ' + card_number[-4:]
        card = UserPaymentMethod(
            person_id=session['user_id'],
            card_number=masked,
            card_type=card_type,
            is_default=False
        )
        db_sess.add(card)
        db_sess.commit()
    return redirect(url_for('profile'))


@app.route('/profile/delete_card/<int:card_id>')
def delete_card(card_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    db_sess = create_session()
    card = db_sess.query(UserPaymentMethod).filter(
        UserPaymentMethod.id == card_id,
        UserPaymentMethod.person_id == session['user_id']
    ).first()
    if card:
        db_sess.delete(card)
        db_sess.commit()
    return redirect(url_for('profile'))


@app.route('/cart')
def cart():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db_sess = create_session()
    cart_items = db_sess.query(Cart).filter(Cart.person_id == session['user_id']).all()

    # Вычисляем общую сумму
    total = sum(item.product.cost * item.amount for item in cart_items)

    return render_template('cart.html', cart_items=cart_items, total=total)


@app.route('/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    form = AddToCartForm()
    if form.validate_on_submit():
        size_id = request.form.get('size_id')  #передаь из формы на странице товара
        if not size_id:
            return "Не выбран размер", 400

        db_sess = create_session()

        existing = db_sess.query(Cart).filter(
            Cart.person_id == session['user_id'],
            Cart.product_id == product_id,
            Cart.size_id == int(size_id)
        ).first()

        if existing:
            existing.amount += form.quantity.data
        else:
            cart_item = Cart(
                person_id=session['user_id'],
                product_id=product_id,
                size_id=int(size_id),
                amount=form.quantity.data
            )
            db_sess.add(cart_item)

        db_sess.commit()
        return redirect(url_for('cart'))

    return redirect(url_for('prod', id=product_id))


@app.route('/cart/update/<int:cart_id>', methods=['POST'])
def update_cart(cart_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db_sess = create_session()
    cart_item = db_sess.query(Cart).filter(
        Cart.id == cart_id,
        Cart.person_id == session['user_id']
    ).first()

    if cart_item:
        new_quantity = request.form.get('quantity', type=int)
        if new_quantity and new_quantity > 0:
            cart_item.amount = new_quantity
            db_sess.commit()

    return redirect(url_for('cart'))


@app.route('/cart/remove/<int:cart_id>')
def remove_from_cart(cart_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db_sess = create_session()
    cart_item = db_sess.query(Cart).filter(
        Cart.id == cart_id,
        Cart.person_id == session['user_id']
    ).first()

    if cart_item:
        db_sess.delete(cart_item)
        db_sess.commit()

    return redirect(url_for('cart'))


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    form = CheckoutForm()
    db_sess = create_session()

    #Получаем товары в корзине
    cart_items = db_sess.query(Cart).filter(Cart.person_id == session['user_id']).all()
    if not cart_items:
        return redirect(url_for('cart'))

    total = sum(item.product.cost * item.amount for item in cart_items)

    if form.validate_on_submit():
        payment_type = db_sess.query(PaymentType).filter(PaymentType.name == form.payment_method.data).first()
        if not payment_type:
            payment_type = PaymentType(name=form.payment_method.data)
            db_sess.add(payment_type)
            db_sess.flush()

        order_type = db_sess.query(OrderType).filter(OrderType.name == 'Новый').first()
        if not order_type:
            order_type = OrderType(name='Новый')
            db_sess.add(order_type)
            db_sess.flush()

        order = Order(
            person_id=session['user_id'],
            payment_type_id=payment_type.id,
            order_type_id=order_type.id
        )
        db_sess.add(order)
        db_sess.flush()

        #в order_items
        for item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                size_id=item.size_id,
                amount=item.amount,
                price=item.product.cost
            )
            db_sess.add(order_item)
            db_sess.delete(item)

        db_sess.commit()
        return redirect(url_for('order_status', order_id=order.id))

    return render_template('payout.html', form=form, cart_items=cart_items, total=total)


@app.route('/payout')
def payout():
    checkout_form = CheckoutForm()
    return render_template('payout.html', form=checkout_form)


@app.route('/order_status/<int:order_id>')
def order_status(order_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    db_sess = create_session()
    order = db_sess.query(Order).filter(Order.id == order_id, Order.person_id == session['user_id']).first()
    if not order:
        return "Заказ не найден"
    return render_template('order_status.html', order=order)


if __name__ == '__main__':
    app.run(debug=True, port=8010)