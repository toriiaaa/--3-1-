from database.database import DataBase


class DataBaseHandler(DataBase):

    def get_suppliers(self):
        self.cursor.execute("SELECT SupplierName FROM Suppliers ORDER BY SupplierName")
        return [x[0] for x in self.cursor.fetchall()]

    def get_categories(self):
        self.cursor.execute("SELECT CategoryName FROM Categories ORDER BY CategoryName")
        return [x[0] for x in self.cursor.fetchall()]

    def get_products(self):
        self.cursor.execute("SELECT ProductID, ProductName FROM Products ORDER BY ProductName")
        return self.cursor.fetchall()

    def filter_products_by_name(self, part_of_name):
        query = f"SELECT * FROM Products WHERE ProductName LIKE ? ORDER BY ProductName"
        self.cursor.execute(query, '%' + part_of_name + '%')
        return self.cursor.fetchall()

    # Получение товара по id
    def get_detail_product(self, pk):
        query = "SELECT * FROM Products WHERE ProductID = ?"
        self.cursor.execute(query, pk)
        product = [*self.cursor.fetchone()]
        price = product[5]
        product[2] = self.get_supplier_name_by_id(product[2])
        product[3] = self.get_category_name_by_id(product[3])
        product[5] = float(price)
        return product

    def get_supplier_name_by_id(self, pk):
        query = "SELECT SupplierName FROM Suppliers WHERE SupplierID = ?"
        self.cursor.execute(query, pk)
        supplier = self.cursor.fetchone()
        return supplier.SupplierName if supplier else -1

    def get_category_name_by_id(self, pk):
        query = "SELECT CategoryName FROM Categories WHERE CategoryID = ?"
        self.cursor.execute(query, pk)
        category = self.cursor.fetchone()
        return category.CategoryName if category else -1

    # Сохранение товара
    def save_product(self, pk, name, supplier, category, quantity, price):
        supplier_id = self.get_supplier_id_by_name(supplier)
        category_id = self.get_category_id_by_name(category)
        query = "UPDATE Products SET ProductName=?, SupplierID=?, CategoryID=?, QuantityPerUnit=?, UnitPrice=? WHERE " \
                "ProductID=? "
        self.cursor.execute(query, (name, supplier_id, category_id, quantity, price, pk))
        r = self.connection.commit()

    def get_supplier_id_by_name(self, name):
        query = "SELECT SupplierID FROM Suppliers WHERE SupplierName = ?"
        self.cursor.execute(query, name)
        supplier = self.cursor.fetchone()
        return supplier.SupplierID if supplier else -1

    def get_category_id_by_name(self, name):
        query = "SELECT CategoryID FROM Categories WHERE CategoryName = ?"
        self.cursor.execute(query, name)
        category = self.cursor.fetchone()
        return category.CategoryID if category else -1

    # Удаление товара
    def delete_product_by_id(self, pk):
        query = "DELETE FROM Products WHERE ProductID=?"
        self.cursor.execute(query, pk)
        self.connection.commit()

    # Создание товара
    def create_product(self, name, supplier, category, quantity, price):
        supplier_id = self.get_supplier_id_by_name(supplier)
        category_id = self.get_category_id_by_name(category)
        query = "INSERT INTO Products (ProductName, SupplierID, CategoryID, QuantityPerUnit, UnitPrice) " \
                "VALUES (?, ?, ?, ?, ?)"
        self.cursor.execute(query, (name, supplier_id, category_id, quantity, price))
        self.connection.commit()

        self.cursor.execute("SELECT @@IDENTITY")
        product_id = self.cursor.fetchone()[0]
        return product_id
# SELECT Suppliers.SupplierID, Suppliers.SupplierName, Suppliers.SupplierID FROM Suppliers ORDER BY Suppliers.[SupplierName];
