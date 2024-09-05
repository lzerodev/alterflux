from PyQt5.QtWidgets import QDialog, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QIcon

from .transaction_dialog import TransactionDialog

from database import session
from database.models import Product, Transaction

class TransactionList(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Fluxo de Caixa')
        self.setGeometry(self.geometry().width()//2, self.geometry().height()//2, 1360, 260)

        self.setWindowIcon(QIcon('resources/assets/icons/money.svg'))

        with open("resources/styles.qss", "r") as f:
            self.setStyleSheet(f.read())        
    
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.add_button = QPushButton('Registrar Transação')
        self.add_button.clicked.connect(self.add_transaction)
        self.layout.addWidget(self.add_button)

        self.table = QTableWidget()
        self.table.setColumnCount(6)

        self.table.setColumnWidth(0, self.geometry().width()//8 - 20)
        self.table.setColumnWidth(1, self.geometry().width()//8 - 10)
        self.table.setColumnWidth(2, self.geometry().width()//8 - 10)
        self.table.setColumnWidth(3, self.geometry().width()//8 - 10)
        self.table.setColumnWidth(4, self.geometry().width()//8 - 10)
        self.table.setColumnWidth(5, self.geometry().width()//8 - 10)

        self.table.setHorizontalHeaderLabels(['Produto', 'Quantidade', 'Forma de Pagamento', 'Data', 'Valor Unitário', 'Total Venda'])
        self.layout.addWidget(self.table)

        self.load_data()

    def load_data(self):
        self.table.setRowCount(0)

        transactions = session.query(Transaction).all()

        for transaction in transactions:
            product = session.query(Product).get(transaction.product_id)
            product_name = product.name if product else "Produto Desconhecido"
            product_price = product.price if product else 0

            total_item = transaction.quantity * product_price

            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(product_name))
            self.table.setItem(row_position, 1, QTableWidgetItem(str(transaction.quantity)))
            self.table.setItem(row_position, 2, QTableWidgetItem(transaction.transaction_type))
            self.table.setItem(row_position, 3, QTableWidgetItem(transaction.date.strftime('%d/%m/%Y %H:%M:%S')))
            self.table.setItem(row_position, 4, QTableWidgetItem(f"R$ {product_price:.2f}"))
            self.table.setItem(row_position, 5, QTableWidgetItem(f"R$ {total_item:.2f}"))

    def add_transaction(self):
        dialog = TransactionDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            transaction = Transaction(
                product_id=data['product_id'],
                quantity=data['quantity'],
                transaction_type=data['transaction_type']
            )
            session.add(transaction)
            session.commit()
            self.load_data()
