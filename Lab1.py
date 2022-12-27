from PyQt6.QtWidgets import QPushButton, QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
import sys

WINDOW_TITLE = 'GUI - Qt.Lab1'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(WINDOW_TITLE)

        button = QPushButton("Нажми меня!")
        button.setCheckable(True)
        button.clicked.connect(self.the_button_was_clicked)
      
        self.label = QLabel()
        layout = QVBoxLayout()
        layout.addWidget(button)
        layout.addWidget(self.label)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def the_button_was_clicked(self):
        self.label.setText('Ура Первая Лабораторная сделана!')

if __name__ == '__main__':
    application = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(application.exec())