from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QComboBox, QSpinBox, QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from database import session
from database.models import Product

class StockMovementDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Movimentação de Estoque')
        self.setGeometry(450, 200, 524, 260)
        self.setWindowIcon(QIcon('resources/assets/icons/stock.svg'))

        with open("resources/styles.qss", "r") as f:
            self.setStyleSheet(f.read())        

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        form_layout = QFormLayout()

        self.product_input = QComboBox()
        products = session.query(Product).all()
        for product in products:
            self.product_input.addItem(product.name, product.id)

        self.quantity_input = QSpinBox()
        self.quantity_input.setMinimum(1)

        self.movement_type_input = QComboBox()
        self.movement_type_input.addItems(['Entrada', 'Saída'])

        form_layout.addRow('Produto:', self.product_input)
        form_layout.addRow('Quantidade:', self.quantity_input)
        form_layout.addRow('Tipo de Movimentação:', self.movement_type_input)

        self.layout.addLayout(form_layout)

        self.save_button = QPushButton('Registrar Movimentação')
        self.cancel_button = QPushButton('Cancelar')

        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        button_layout = QVBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        self.layout.addLayout(button_layout)

    def get_data(self):
        return {
            'product_id': self.product_input.currentData(),
            'quantity': self.quantity_input.value(),
            'movement_type': self.movement_type_input.currentText()
        }
