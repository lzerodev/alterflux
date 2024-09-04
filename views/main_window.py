from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from views.product.product_list import ProductList
from views.reports.report_view import ReportWindow
from views.stock.stock_movement_list import StockMovementList
from views.transaction.transction_list import TransactionList

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('AlterFlux - 2024')
        self.setGeometry(self.geometry().width()//2, self.geometry().height()//2, 1024, 560)
        # self.showMaximized()

        self._central_widget = QWidget()
        self.setCentralWidget(self._central_widget)

        self.layout = QVBoxLayout()
        self._central_widget.setLayout(self.layout)

        self.setWindowIcon(QIcon('resources/assets/icons/cashbox.svg'))

        self._create_ui()

        with open("resources/styles.qss", "r") as f:
            self.setStyleSheet(f.read())

    def _create_ui(self):

        products_button = QPushButton('Gerenciar Produtos')
        stock_button = QPushButton('Movimentação de Estoque')
        transaction_button = QPushButton('Fluxo de Caixa')
        reports_button = QPushButton('Relatórios')
        exit_button = QPushButton('Sair')

        products_button.clicked.connect(self.manage_products)
        stock_button.clicked.connect(self.manage_stock)
        transaction_button.clicked.connect(self.manage_transaction)
        reports_button.clicked.connect(self.view_reports)
        exit_button.clicked.connect(self.close)

        self.layout.addWidget(products_button)
        self.layout.addWidget(stock_button)
        self.layout.addWidget(transaction_button)
        self.layout.addWidget(reports_button)
        self.layout.addWidget(exit_button)
        
        self.layout.setAlignment(Qt.AlignCenter)


    def manage_products(self):
        self.product_list = ProductList()
        self.product_list.show()

    def manage_stock(self):
        self.stock_movement_list = StockMovementList()
        self.stock_movement_list.show()

    def manage_transaction(self):
        self.transaction_list = TransactionList()
        self.transaction_list.show()

    def view_reports(self):
        self.report_window = ReportWindow()
        self.report_window.show()