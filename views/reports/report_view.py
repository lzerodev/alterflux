from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QDateEdit, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QIcon

from database import session
from database.models import Transaction, Product

from datetime import datetime

class ReportWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Relatório de Transações')
        self.setGeometry(self.geometry().width()//2, self.geometry().height()//2, 1360, 260)
        
        self.setWindowIcon(QIcon('resources/assets/icons/report.svg'))

        with open("resources/styles.qss", "r") as f:
            self.setStyleSheet(f.read())        

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.start_date_label = QLabel('Data Inicial:')
        self.layout.addWidget(self.start_date_label)

        self.start_date_edit = QDateEdit()
        self.start_date_edit.setDate(QDate.currentDate())
        self.layout.addWidget(self.start_date_edit)

        self.end_date_label = QLabel('Data Final:')
        self.layout.addWidget(self.end_date_label)

        self.end_date_edit = QDateEdit()
        self.end_date_edit.setDate(QDate.currentDate())
        self.layout.addWidget(self.end_date_edit)

        self.generate_button = QPushButton('Gerar Relatório')
        self.generate_button.clicked.connect(self.generate_report)
        self.layout.addWidget(self.generate_button)

        self.table = QTableWidget()
        self.table.setColumnCount(7)

        self.table.setColumnWidth(0, self.geometry().width()//8 - 20)
        self.table.setColumnWidth(1, self.geometry().width()//8 - 10)
        self.table.setColumnWidth(2, self.geometry().width()//8 - 10)
        self.table.setColumnWidth(3, self.geometry().width()//8 - 10)
        self.table.setColumnWidth(4, self.geometry().width()//8 - 10)
        self.table.setColumnWidth(5, self.geometry().width()//8 - 10)
        self.table.setColumnWidth(6, self.geometry().width()//8 - 10)
        self.table.setColumnWidth(7, self.geometry().width()//8 - 10)

        self.table.setHorizontalHeaderLabels(['Produto', 'Quantidade', 'Tipo', 'Data', 'Valor Unitário', 'Total Item', 'Total Geral'])
        self.layout.addWidget(self.table)

    def generate_report(self):
        start_date = self.start_date_edit.date().toPyDate()
        end_date = self.end_date_edit.date().toPyDate()

        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.max.time())

        transactions = session.query(Transaction).filter(Transaction.date.between(start_datetime, end_datetime)).all()

        self.table.setRowCount(0)
        total_geral = 0

        self.table.setRowCount(0)
        for transaction in transactions:
            product = session.query(Product).get(transaction.product_id)
            product_name = product.name if product else "Produto Desconhecido"
            product_price = product.price if product else 0

            total_item = transaction.quantity * product_price
            total_geral += total_item

            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(product_name))
            self.table.setItem(row_position, 1, QTableWidgetItem(str(transaction.quantity)))
            self.table.setItem(row_position, 2, QTableWidgetItem(transaction.transaction_type))
            self.table.setItem(row_position, 3, QTableWidgetItem(transaction.date.strftime('%d/%m/%Y %H:%M:%S')))
            self.table.setItem(row_position, 4, QTableWidgetItem(f"R$ {product_price:.2f}"))
            self.table.setItem(row_position, 5, QTableWidgetItem(f"R$ {total_item:.2f}"))
            self.table.setItem(row_position, 6, QTableWidgetItem(f"R$ {total_geral:.2f}"))
