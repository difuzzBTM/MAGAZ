import sys
from data.db_session import global_init, create_session
from data.__all_models import ProductType, Size, Product, ProductSize

DB_PATH = 'db/shop.db'   # укажите точный путь, как в app.py

try:
    global_init(DB_PATH)
    session = create_session()
    print(f"Подключено к {DB_PATH}")
except Exception as e:
    print(f"Ошибка подключения к БД: {e}")
    sys.exit(1)

# Добавление категорий
categories = [
    ('Футболки',),
    ('Джинсы',),
    ('Куртки',),
    ('Платья',),
]

for name in categories:
    if not session.query(ProductType).filter(ProductType.name == name[0]).first():
        cat = ProductType(name=name[0])
        session.add(cat)
        print(f"Добавлена категория: {name[0]}")
session.commit()

# Размеры
size_names = ['XS', 'S', 'M', 'L', 'XL', 'XXL']
sizes_objs = []
for name in size_names:
    size = session.query(Size).filter(Size.name == name).first()
    if not size:
        size = Size(name=name)
        session.add(size)
        session.flush()
        print(f"Добавлен размер: {name}")
    sizes_objs.append(size)
session.commit()

# Функция добавления товара с отладкой
def add_product(name, cost, description, type_name, size_names_list, photos=None):
    try:
        product_type = session.query(ProductType).filter(ProductType.name == type_name).first()
        if not product_type:
            print(f"Ошибка: тип '{type_name}' не найден")
            return

        product = Product(
            name=name,
            cost=cost,
            description=description,
            type_id=product_type.id,
            photos=photos or 'https://via.placeholder.com/400x400/f0f0f0/cccccc?text=No+photo'
        )
        session.add(product)
        session.flush()  # получаем ID

        for size_name in size_names_list:
            size = session.query(Size).filter(Size.name == size_name).first()
            if size:
                ps = ProductSize(product_id=product.id, size_id=size.id)
                session.add(ps)
        session.commit()
        print(f"Товар добавлен: {name}")
    except Exception as e:
        session.rollback()
        print(f"Ошибка при добавлении товара '{name}': {e}")

add_product(
    name='Футболка хлопковая',
    cost=1990,
    description='Удобная футболка из 100% хлопка. Подходит для повседневной носки.',
    type_name='Футболки',
    size_names_list=['S', 'M', 'L', 'XL'],
    photos='https://via.placeholder.com/400x400/f0f0f0/cccccc?text=T-shirt'
)

add_product(
    name='Футболка с принтом',
    cost=2490,
    description='Футболка с ярким принтом. Мягкий материал, современный крой.',
    type_name='Футболки',
    size_names_list=['XS', 'S', 'M', 'L'],
    photos='https://via.placeholder.com/400x400/f0f0f0/cccccc?text=Printed+T-shirt'
)

add_product(
    name='Джинсы прямые',
    cost=3490,
    description='Классические прямые джинсы из плотного денима.',
    type_name='Джинсы',
    size_names_list=['M', 'L', 'XL', 'XXL'],
    photos='https://via.placeholder.com/400x400/f0f0f0/cccccc?text=Jeans'
)

add_product(
    name='Джинсы скинни',
    cost=3990,
    description='Узкие джинсы с высокой посадкой.',
    type_name='Джинсы',
    size_names_list=['S', 'M', 'L'],
    photos='https://via.placeholder.com/400x400/f0f0f0/cccccc?text=Skinny+Jeans'
)

add_product(
    name='Куртка демисезонная',
    cost=5990,
    description='Лёгкая куртка на весну/осень. Ветрозащитная ткань.',
    type_name='Куртки',
    size_names_list=['M', 'L', 'XL'],
    photos='https://via.placeholder.com/400x400/f0f0f0/cccccc?text=Jacket'
)

add_product(
    name='Куртка кожаная',
    cost=12990,
    description='Стильная кожаная куртка из экокожи.',
    type_name='Куртки',
    size_names_list=['S', 'M', 'L'],
    photos='https://via.placeholder.com/400x400/f0f0f0/cccccc?text=Leather+Jacket'
)

add_product(
    name='Платье летнее',
    cost=2990,
    description='Лёгкое платье из натурального хлопка. Идеально для жаркой погоды.',
    type_name='Платья',
    size_names_list=['XS', 'S', 'M', 'L'],
    photos='https://via.placeholder.com/400x400/f0f0f0/cccccc?text=Dress'
)

add_product(
    name='Платье вечернее',
    cost=4590,
    description='Элегантное вечернее платье.',
    type_name='Платья',
    size_names_list=['S', 'M', 'L', 'XL'],
    photos='https://via.placeholder.com/400x400/f0f0f0/cccccc?text=Evening+Dress'
)

print("База данных успешно заполнена тестовыми данными!")
# Добавление товаров (список можно оставить из предыдущего ответа)
# ... (вставьте вызовы add_product из предыдущего скрипта)

print("Готово.")