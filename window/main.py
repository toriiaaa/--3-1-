from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QWidget, QListWidget, QHBoxLayout, \
    QStackedLayout, QComboBox, QSpinBox, QDoubleSpinBox

from database.database_handler import DataBaseHandler


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # ==============
        #   Переменные
        # ==============
        self.db = DataBaseHandler()
        self.current_product = []
        self.product_list = []

        # ======================
        #     Переменные GUI
        # ======================
        # Поиск товара
        self.search_product_input = QLineEdit()
        self.search_product_button = QPushButton('Загрузить')

        # Список товаров
        self.product_list_widget = QListWidget()

        # Навигация для сохранения и отмены изменений
        self.back_button = QPushButton('Назад')
        self.save_button = QPushButton('Сохранить')
        self.delete_button = QPushButton('Удалить')
        self.create_button = QPushButton('Создать')

        # Данные о конкретном товаре
        self.product_name_input = QLineEdit()
        self.suppliers_input = QComboBox()
        self.categories_input = QComboBox()
        self.quantity_perl_input = QSpinBox()
        self.unit_price_input = QDoubleSpinBox()

        # ==================
        #     Наполнение
        # ==================
        # Левая сторона
        self.left_layout = QVBoxLayout()
        self.top_product_layout = QHBoxLayout()
        self.bottom_product_layout = QStackedLayout()

        self._top_product_layout()
        self._bottom_product_layout()

        self.left_layout.addLayout(self.top_product_layout)
        self.left_layout.addLayout(self.bottom_product_layout)

        # Правая сторона
        self.right_layout = QVBoxLayout()
        self.nav_editable_layout = QHBoxLayout()
        self.editable_layout = QVBoxLayout()

        self._nav_editable_layout()
        self._editable_layout()

        self.right_layout.addLayout(self.nav_editable_layout)
        self.right_layout.addLayout(self.editable_layout)

        # ==================
        #     Отрисовка
        # ==================
        self.setWindowTitle('Редактор товаров')

        page_layout = QHBoxLayout()
        page_layout.addLayout(self.left_layout)
        page_layout.addLayout(self.right_layout)

        # Добавление окна в приложение
        container = QWidget()
        container.setLayout(page_layout)
        self.setCentralWidget(container)

    # =================================
    # Отрисовка нижней линии у товара
    def _top_product_layout(self):
        label = QLabel('Товар:')

        self.search_product_button.setCheckable(True)
        self.search_product_button.clicked.connect(self.push_search_product)

        self.top_product_layout.addWidget(label)
        self.top_product_layout.addWidget(self.search_product_input)
        self.top_product_layout.addWidget(self.search_product_button)

    #  Отрисовка нижней линии у товара
    def _bottom_product_layout(self):
        self.product_list = self.db.get_products()
        only_names = self.get_names_products(self.product_list)

        self.product_list_widget.addItems(only_names)
        self.product_list_widget.itemClicked.connect(self.get_current_product)
        self.bottom_product_layout.addWidget(self.product_list_widget)

    # Навигационные кнопки для формы
    def _nav_editable_layout(self):
        # Кнопка назад
        self.back_button.setCheckable(True)
        self.back_button.clicked.connect(self.push_cancel)
        self.nav_editable_layout.addWidget(self.back_button)

        # Кнопка сохранить
        self.save_button.setCheckable(True)
        self.save_button.clicked.connect(self.push_save)
        self.nav_editable_layout.addWidget(self.save_button)

        # Кнопка удалить
        self.delete_button.setCheckable(True)
        self.delete_button.clicked.connect(self.push_delete)
        self.nav_editable_layout.addWidget(self.delete_button)

        # Кнопка создать
        self.create_button.setCheckable(True)
        self.create_button.clicked.connect(self.push_create)
        self.nav_editable_layout.addWidget(self.create_button)

    # Отрисовка формы для редактирования
    def _editable_layout(self):
        # Редактирование продукта
        product_name_layout = QHBoxLayout()
        product_name_label = QLabel('Название товара:')
        product_name_layout.addWidget(product_name_label)
        product_name_layout.addWidget(self.product_name_input)
        self.editable_layout.addLayout(product_name_layout)

        # Выбор поставщика
        suppliers_layout = QHBoxLayout()
        suppliers_label = QLabel('Поставщик:')
        self.suppliers_input.addItems(self.db.get_suppliers())
        suppliers_layout.addWidget(suppliers_label)
        suppliers_layout.addWidget(self.suppliers_input)
        self.editable_layout.addLayout(suppliers_layout)

        # Выбор категории
        categories_layout = QHBoxLayout()
        categories_label = QLabel('Категория:')
        self.categories_input.addItems(self.db.get_categories())
        categories_layout.addWidget(categories_label)
        categories_layout.addWidget(self.categories_input)
        self.editable_layout.addLayout(categories_layout)

        # Ввод количество на единицу
        quantity_perl_layout = QHBoxLayout()
        quantity_perl_label = QLabel('Количество на единицу:')
        quantity_perl_layout.addWidget(quantity_perl_label)
        quantity_perl_layout.addWidget(self.quantity_perl_input)
        self.editable_layout.addLayout(quantity_perl_layout)

        # Ввод цены за единицу
        unit_price_layout = QHBoxLayout()
        unit_price_label = QLabel('Цена за единицу:')
        unit_price_layout.addWidget(unit_price_label)
        self.unit_price_input.setMaximum(1000000000.0)
        unit_price_layout.addWidget(self.unit_price_input)
        self.editable_layout.addLayout(unit_price_layout)

    # =================================
    # Клик на кнопку search_product
    def push_search_product(self):
        filter_text = self.search_product_input.text().lower()
        self.product_list = self.db.filter_products_by_name(filter_text)
        names = self.get_names_products(self.product_list)
        self.product_list_widget.clear()
        self.product_list_widget.addItems(names)

    # Получение продукта после нажатия на запись в списке
    def get_current_product(self, item):
        selected_index = self.product_list_widget.row(item)
        product = self.product_list[selected_index]
        data_product = self.db.get_detail_product(product[0])
        self.current_product = data_product
        self.set_form(data_product)

    # Сохранить
    def push_save(self):
        result = self.get_data_from_form()
        if result[0] == -1:
            return
        self.db.save_product(*result)
        self.current_product = result
        self.push_search_product()

    # Назад
    def push_cancel(self):
        self.set_form(self.current_product)

    # Удаление
    def push_delete(self):
        form_data = self.get_data_from_form()
        if form_data[0] == -1:
            return
        self.db.delete_product_by_id(form_data[0])
        self.clear_form()
        self.current_product = []
        self.push_search_product()

    # Создание
    def push_create(self):
        result = self.get_data_from_form()
        new_product_id = self.db.create_product(*result[1:])
        self.current_product = [new_product_id]
        self.current_product = self.get_data_from_form()
        self.push_search_product()

    def push_exit(self):
        if self.is_empty_form() or len(self.current_product) < 5:
            return
        self.push_save()

    # =================================
    # ОБЩИЕ ФУНКЦИИ
    def set_form(self, product):
        self.product_name_input.setText(product[1])
        self.suppliers_input.setCurrentText(product[2])
        self.categories_input.setCurrentText(product[3])
        self.quantity_perl_input.setValue(product[4])
        self.unit_price_input.setValue(product[5])

    # Получение данных из формы
    def get_data_from_form(self):
        pk = -1
        print(self.current_product)
        if len(self.current_product):
            pk = self.current_product[0]
        return [
            pk,
            self.product_name_input.text(),
            self.suppliers_input.currentText(),
            self.categories_input.currentText(),
            self.quantity_perl_input.text(),
            self.unit_price_input.text(),
        ]

    # Очистка данных из формы
    def clear_form(self):
        self.product_name_input.clear()
        self.suppliers_input.setCurrentIndex(0)
        self.categories_input.setCurrentIndex(0)
        self.quantity_perl_input.clear()
        self.unit_price_input.clear()

    def is_empty_form(self):
        form_data = self.get_data_from_form()
        return (
                not form_data[0]
                and not form_data[1]
                and form_data[2] == self.suppliers_input.itemText(0)
                and form_data[3] == self.categories_input.itemText(0)
                and form_data[4] == 0
                and int(form_data[5]) == 0
        )

    @staticmethod
    def get_names_products(products: list):
        return [x[1] for x in products]
