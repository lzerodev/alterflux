from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QSpinBox, QComboBox, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class TransactionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Registrar Transação Financeira')
        self.setGeometry(450, 200, 524, 260)
        self.setWindowIcon(QIcon('resources/assets/icons/money.svg'))

        with open("resources/styles.qss", "r") as f:
            self.setStyleSheet(f.read())        

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        form_layout = QFormLayout()

        self.product_id_input = QLineEdit()
        self.quantity_input = QSpinBox()
        self.quantity_input.setMaximum(1000000)

        self.payment_type_input = QComboBox()
        self.payment_type_input.addItems(['Crédito', 'Débito', 'Pix', 'Dinheiro'])

        form_layout.addRow('ID do Produto:', self.product_id_input)
        form_layout.addRow('Quantidade:', self.quantity_input)
        form_layout.addRow('Forma de pagamento:', self.payment_type_input)

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
            'product_id': self.product_id_input.text(),
            'quantity': self.quantity_input.value(),
            'payment_type': self.payment_type_input.currentText()
        }
