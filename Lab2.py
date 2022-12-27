import sys
from PyQt6 import QtWidgets

from PyQt6.QtCore import QRect, pyqtSignal, QObject
from PyQt6.QtWidgets import QApplication, QPushButton, QLineEdit, QLabel

WINDOW_TITLE = 'GUI - Qt.Lab2'
WINDOW_WIDTH = 360
WINDOW_HEIGHT = 200

class money_state_signal(QObject):
    update_signal = pyqtSignal(float,float)


class usd_holder:
    def __init__(self):
        super().__init__()
        self.value = ''

    def update_value(self, k_value: float, money: float):
        self.value = str(money / k_value)


class rub_holder:
    def __init__(self):
        super().__init__()
        self.value = ''

    def update_value(self, k_value: float, money: float):
        self.value = str(money * k_value)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.k = 2
        self.rub = 2
        self.usd = self.rub / self.k
        self.oil = 1

        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.rub_holder = rub_holder()
        self.usd_holder = usd_holder()
        self.rubStateSignal = money_state_signal()
        self.usdStateSignal = money_state_signal()

        self.kLabel = QLabel(self)
        self.kLabel.setText("Коэффициент")
        self.kLabel.setGeometry(QRect(10, 10, 150, 25))
        self.kLineEdit = QLineEdit(self)
        self.kLineEdit.setGeometry(QRect(120, 10, 220, 25))

        self.oilLabel = QLabel(self)
        self.oilLabel.setText("Стоимость нефти")
        self.oilLabel.setGeometry(QRect(10, 40, 150, 25)) 
        self.oilLineEdit = QLineEdit(self)
        self.oilLineEdit.setGeometry(QRect(120, 40, 220, 25))

        self.rubLabel = QLabel(self)
        self.rubLabel.setText("Рубль")
        self.rubLabel.setGeometry(QRect(10, 70, 150, 25))
        self.rubLineEdit = QLineEdit(self)
        self.rubLineEdit.setGeometry(QRect(120, 70, 220, 25))
        self.rubLineEdit.setReadOnly(True)

        self.usdLabel = QLabel(self)
        self.usdLabel.setText("Доллар")
        self.usdLabel.setGeometry(QRect(10, 100, 150, 25))
        self.usdLineEdit = QLineEdit(self)
        self.usdLineEdit.setGeometry(QRect(120, 100, 220, 25))
        self.usdLineEdit.setReadOnly(True)

        self.convertButton = QPushButton(self)
        self.convertButton.setText("Расчитать курс валют")
        self.convertButton.setGeometry(QRect(80, 140, 200, 50))

        self.kLineEdit.setText(str(self.k))
        self.oilLineEdit.setText(str(self.oil))
        self.rubLineEdit.setText(str(self.rub))
        self.usdLineEdit.setText(str(self.usd))

        self.rubStateSignal.update_signal.connect(self.rub_holder.update_value)
        self.usdStateSignal.update_signal.connect(self.usd_holder.update_value)

        self.convertButton.clicked.connect(self.on_convert_button_click)

        self.show()

    def on_convert_button_click(self):
        curr_oil = float(self.oil)
        
        k_value = self.str_val_convert_to_float(self.kLineEdit.text())
        oil_value = self.str_val_convert_to_float(self.oilLineEdit.text())

        rub_value = self.str_val_convert_to_float(self.rubLineEdit.text())
        usd_value = self.str_val_convert_to_float(self.usdLineEdit.text())
   
        if curr_oil < oil_value:
            self.usdStateSignal.update_signal.emit(k_value, rub_value)
            self.usdLineEdit.setText(self.usd_holder.value)
            self.rubLineEdit.setText(str(rub_value + oil_value))
        elif curr_oil > oil_value:
            self.rubStateSignal.update_signal.emit(k_value, usd_value)
            self.rubLineEdit.setText(self.usd_holder.value)
            self.usdLineEdit.setText(str(usd_value + oil_value))
        else:
            oil_value = curr_oil

        self.oil = float(oil_value)

    def str_val_convert_to_float(self, val: str):
        
        if val is None or len(val) == 0:
            value = 0
        else:
            value = float(val)

        return value

if __name__ == '__main__':
    application = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(application.exec())