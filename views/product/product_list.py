from sqlite3 import IntegrityError
from PyQt5.QtWidgets import QDialog, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt5.QtGui import QIcon

from .product_dialog import ProductDialog

from database import session
from database.models import Product

class ProductList(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Gerenciar Produtos')

        self.setGeometry(self.geometry().width()//2, self.geometry().height()//2, 1360, 260)

        self.setWindowIcon(QIcon('resources/assets/icons/product.svg'))

        with open("resources/styles.qss", "r") as f:
            self.setStyleSheet(f.read())

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        button_layout = QHBoxLayout()

        self.add_button = QPushButton('Adicionar Produto')
        self.edit_button = QPushButton('Editar Produto')
        self.delete_button = QPushButton('Excluir Produto')

        self.add_button.clicked.connect(self.add_product)
        self.edit_button.clicked.connect(self.edit_product)
        self.delete_button.clicked.connect(self.delete_product)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)

        self.layout.addLayout(button_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(4)

        self.table.setColumnWidth(0, self.geometry().width()//8 - 20)
        self.table.setColumnWidth(1, self.geometry().width()//5 - 10)
        self.table.setColumnWidth(2, self.geometry().width()//8 - 10)
        self.table.setColumnWidth(3, self.geometry().width()//8 - 10)
        self.table.setColumnWidth(4, self.geometry().width()//8 - 10)

        self.table.setHorizontalHeaderLabels(['Nome', 'Descrição', 'Quantidade', 'Preço'])
        self.layout.addWidget(self.table)

        self.load_data()

    def load_data(self):
        self.table.setRowCount(0)
        products = session.query(Product).all()
        for product in products:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(product.name))
            self.table.setItem(row_position, 1, QTableWidgetItem(product.description))
            self.table.setItem(row_position, 2, QTableWidgetItem(str(product.quantity)))
            self.table.setItem(row_position, 3, QTableWidgetItem(f'R${product.price:.2f}'))

    def add_product(self):
        dialog = ProductDialog(self)
        if dialog.exec() == QDialog.accepted:
            data = dialog.get_data()
            product = Product(
                name=data['name'],
                description=data['description'],
                quantity=data['quantity'],
                price=data['price']
            )
            session.add(product)
            session.commit()
            self.load_data()

    def edit_product(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, 'Aviso', 'Selecione um produto para editar.')
            return

        product = session.query(Product).all()[selected_row]

        dialog = ProductDialog(self)
        dialog.set_data({
            'name': product.name,
            'description': product.description,
            'quantity': product.quantity,
            'price': product.price
        })

        if dialog.exec() == QDialog.accepted:
            data = dialog.get_data()
            product.name = data['name']
            product.description = data['description']
            product.quantity = data['quantity']
            product.price = data['price']
            session.commit()
            self.load_data()

    def delete_product(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, 'Aviso', 'Selecione um produto para excluir.')
            return

        product = session.query(Product).all()[selected_row]

        reply = QMessageBox.question(self, 'Confirmação', f'Tem certeza que deseja excluir o produto {product.name}?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            try: 
                session.delete(product)
                session.commit()
                self.load_data()
                QMessageBox.information(self, 'Sucesso', f'O produto {product.name} excluído com sucesso')
            except IntegrityError:
                session.rollback() 
                QMessageBox.critical(self, 'Erro', 'Não é possível excluir um item com estoque')
