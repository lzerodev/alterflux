from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QSpinBox, QDoubleSpinBox, QPushButton
from PyQt5.QtGui import QIcon


class ProductDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Produto')
        self.setGeometry(450, 200, 524, 260)
        self.setWindowIcon(QIcon('resources/assets/icons/product.svg'))
               
        with open("resources/styles.qss", "r") as f:
            self.setStyleSheet(f.read())

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        form_layout = QFormLayout()

        self.name_input = QLineEdit()
        self.description_input = QLineEdit()
        self.quantity_input = QSpinBox()
        self.quantity_input.setMinimum(0)
        self.price_input = QDoubleSpinBox()
        self.price_input.setMinimum(0.0)
        self.price_input.setMaximum(1000000.0)
        self.price_input.setDecimals(2)

        form_layout.addRow('Nome:', self.name_input)
        form_layout.addRow('Descrição:', self.description_input)
        form_layout.addRow('Quantidade:', self.quantity_input)
        form_layout.addRow('Preço:', self.price_input)

        self.layout.addLayout(form_layout)

        self.save_button = QPushButton('Salvar')
        self.cancel_button = QPushButton('Cancelar')

        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        button_layout = QVBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        self.layout.addLayout(button_layout)

    def get_data(self):
        return {
            'name': self.name_input.text(),
            'description': self.description_input.text(),
            'quantity': self.quantity_input.value(),
            'price': self.price_input.value(),
        }

    def set_data(self, data):
        self.name_input.setText(data['name'])
        self.description_input.setText(data['description'])
        self.quantity_input.setValue(data['quantity'])
        self.price_input.setValue(data['price'])
