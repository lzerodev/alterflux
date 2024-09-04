from PyQt5.QtWidgets import QDialog,QMessageBox, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from .stock_movement_dialog import StockMovementDialog

from database import session
from database.models import Product, StockMovement

class StockMovementList(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Movimentação de Estoque')

        self.setGeometry(self.geometry().width()//2, self.geometry().height()//2, 1360, 260)

        self.setWindowIcon(QIcon('resources/assets/icons/stock.svg'))

        with open("resources/styles.qss", "r") as f:
            self.setStyleSheet(f.read())

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.add_button = QPushButton('Registrar Movimentação')
        self.add_button.clicked.connect(self.add_movement)
        self.layout.addWidget(self.add_button)

        self.table = QTableWidget()
        self.table.setColumnCount(4)

        self.table.setColumnWidth(0, self.geometry().width()//8 - 20)
        self.table.setColumnWidth(1, self.geometry().width()//8 - 10)
        self.table.setColumnWidth(2, self.geometry().width()//8 - 10)
        self.table.setColumnWidth(3, self.geometry().width()//8 - 10)
        self.table.setColumnWidth(4, self.geometry().width()//8 - 10)

        self.table.setHorizontalHeaderLabels(['Produto', 'Quantidade', 'Tipo de Movimentação', 'Data'])
        self.layout.addWidget(self.table)

        self.load_data()

    def load_data(self):
        self.table.setRowCount(0)
        movements = session.query(StockMovement).all()
        for movement in movements:
            product = session.query(Product).filter(Product.id == movement.product_id).first()
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(product.name))
            self.table.setItem(row_position, 1, QTableWidgetItem(str(movement.quantity)))
            self.table.setItem(row_position, 2, QTableWidgetItem(movement.movement_type))
            self.table.setItem(row_position, 3, QTableWidgetItem(movement.date.strftime('%d/%m/%Y %H:%M:%S')))

    def add_movement(self):
        dialog = StockMovementDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            product = session.query(Product).filter(Product.id == data['product_id']).first()

            if data['movement_type'] == 'Entrada':
                product.quantity += data['quantity']
            else:
                if product.quantity >= data['quantity']:
                    product.quantity -= data['quantity']
                else:
                    QMessageBox.warning(self, 'Erro', 'Quantidade insuficiente em estoque.')
                    return

            movement = StockMovement(
                product_id=data['product_id'],
                quantity=data['quantity'],
                movement_type=data['movement_type']
            )

            session.add(movement)
            session.commit()
            self.load_data()
