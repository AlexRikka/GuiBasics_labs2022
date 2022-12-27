import os
import sys
import PyQt6
import traceback
from PyQt6.QtCore import QThread 
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenuBar, QStatusBar, QWidget, QPushButton, QLabel
from PyQt6.QtWidgets import QComboBox, QTabWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# GLOBAL PARAMS
WINDOW_TITLE = 'GUI - Qt.Lab3'
WINDOW_WIDTH = 816
WINDOW_HEIGHT = 489
DB_STATUS = 'Состояние подключения к БД: '
DB = os.path.join(os.path.dirname(__file__), 'ANIME.db')

class T_ANIME(Base):
    __tablename__ = 'T_ANIME'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    genre = Column(String(100))
    rating = Column(String(100))
    type = Column(String(100))

    def init(self, id, name, genre, rating, type):
        self.id = id
        self.name = name
        self.genre = genre
        self.rating = rating
        self.type = type

class QueryRunner(QThread):
    def __init__(self, query, parent=None):
        super(QueryRunner, self).__init__(parent)
        self.query = query
        return 
    
    def run(self):
        self.query.exec()

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle(WINDOW_TITLE)
        self.setMinimumSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        # Main Menu Widget
        self.main_menu = QMenuBar()
        self.setMenuBar(self.main_menu)
        # FILE SubMenu
        m = self.main_menu.addMenu("Файл")
        self.exit_action = m.addAction("Выход")
        # DB SubMenu
        m = self.main_menu.addMenu("База данных")
        self.set_connetcion_action = m.addAction("Установить соединение")
        self.close_connetcion_action = m.addAction("Закрыть соединение")
        self.close_connetcion_action.setEnabled(False)
        
        # Main Menu Action
        self.exit_action.triggered.connect(self.exit_app)
        self.set_connetcion_action.triggered.connect(self.connect_db)
        self.close_connetcion_action.triggered.connect(self.disconnect_db)

        # Main Window Widget 
        self.main_widget = QWidget()
        # Main Window Layouts
        self.grid_layout = QGridLayout()
        self.hbox_layout = QHBoxLayout()
        self.vbox_layout = QVBoxLayout()

        # Query Buttons
        self.query1_button = QPushButton()
        self.query3_button = QPushButton()
        self.query4_button = QPushButton()
        
        self.query1_button.setText("Получить названия аниме")
        self.query3_button.setText("Получить рейтинги аниме")
        self.query4_button.setText("Получить жанры аниме")

        self.query1_button.setEnabled(False)
        self.query3_button.setEnabled(False)
        self.query4_button.setEnabled(False)
    
        # Query Buttons Action
        self.query1_button.clicked.connect(self.get_name)
        self.query3_button.clicked.connect(self.get_rating)
        self.query4_button.clicked.connect(self.get_genre)

        # Query Conmbo Box
        self.query2_combobox = QComboBox()
        self.query2_combobox.addItems([''])
        self.query2_combobox.setEnabled(False)

        # Query Conmbo Box Action
        self.query2_combobox.currentIndexChanged.connect(self.combobox_selection_change)

        # Tab Widget
        self.tab = QTabWidget()
        self.record_list = []

        self.is_construct = False

        self.tab_full_table = QTableWidget() 
        self.tab_full = 'Поный список аниме &1'
        self.construct_table('FULL')

        self.tab_name_table = QTableWidget() 
        self.tab_name = 'Наименование аниме &2'
        self.construct_table('NAME')

        self.tab_type_table = QTableWidget() 
        self.tab_type = 'Аниме по типам &3'
        self.construct_table('TYPE')
        
        self.tab_rating_table = QTableWidget() 
        self.tab_rating = 'Рейтинг аниме &4'
        self.construct_table('RATING')

        self.tab_genre_table = QTableWidget() 
        self.tab_genre = 'Жанры аниме &5'
        self.construct_table('GENRE')

        self.tab.setCurrentIndex(0)

        # Status Bar Widget
        self.db_state_label = QLabel()
        self.db_state_value = QLabel()
        self.status_bar = QStatusBar()
        self.status_bar.showMessage(DB_STATUS + 'Соединение отсутсвует')
    
        # Construct Layouts
        self.grid_layout.addWidget(self.query1_button, 0, 0)
        self.grid_layout.addWidget(self.query2_combobox, 0, 1)
        self.grid_layout.addWidget(self.query3_button, 1, 0)
        self.grid_layout.addWidget(self.query4_button, 1, 1)
        self.grid_layout.addWidget(self.query4_button, 1, 1)
        self.hbox_layout.addWidget(self.tab)
        
        self.vbox_layout.addItem(self.grid_layout)
        
        self.vbox_layout.addItem(self.hbox_layout)
        self.vbox_layout.addWidget(self.status_bar)

        self.main_widget.setLayout(self.vbox_layout)
        self.setCentralWidget(self.main_widget)

    def connect_db(self):
        self.is_construct = True
        self.set_connetcion_action.setEnabled(False)
        self.close_connetcion_action.setEnabled(True)
        self.query1_button.setEnabled(True)
        self.query2_combobox.setEnabled(True)
        self.query3_button.setEnabled(True)
        self.query4_button.setEnabled(True)
        self.engine = create_engine(f'sqlite:///' + DB , echo=False) 
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        try:
            self.record_list = self.session.query(T_ANIME).all()
        except Exception:
            traceback.print_exc()
            return None

        items = []
        for r, data in enumerate(self.record_list):
            if data.type not in items :
                items += [data.type]
        
        self.query2_combobox.addItems(items)
        self.query2_combobox.setCurrentText('')
        self.query2_combobox.removeItem(self.query2_combobox.currentIndex())
        self.construct_table('FULL')
        self.is_construct = False
        self.status_bar.showMessage(DB_STATUS + 'Подключено')

    def disconnect_db(self):
        self.session.close()
        self.engine.dispose()
        self.status_bar.showMessage(DB_STATUS + 'Отсутсвует')
        self.set_connetcion_action.setEnabled(True)
        self.close_connetcion_action.setEnabled(False)
        self.query1_button.setEnabled(False)
        self.query2_combobox.setEnabled(False)
        self.query3_button.setEnabled(False)
        self.query4_button.setEnabled(False)

        while self.query2_combobox.count() > 0:
            self.query2_combobox.removeItem(0)

        self.query2_combobox.addItems([''])

        self.record_list = []
        self.construct_table('FULL')
        self.construct_table('NAME')
        self.construct_table('TYPE')
        self.construct_table('RATING')
        self.construct_table('GENRE')
        
        self.tab.setCurrentIndex(0)

    def combobox_selection_change(self, i):
        if self.is_construct == False: 
            self.record_list = self.session.query(T_ANIME).filter_by(type=self.query2_combobox.currentText()).all()
            self.construct_table('TYPE')

    def get_name(self):
        if self.is_construct == False: 
            self.record_list = self.session.query(T_ANIME).all()
            self.construct_table('NAME')

    def get_rating(self):
        if self.is_construct == False: 
            self.record_list = self.session.query(T_ANIME).all()
            self.construct_table('RATING')

    def get_genre(self):
        if self.is_construct == False: 
            self.record_list = self.session.query(T_ANIME).all()
            self.construct_table('GENRE')

    def exit_app(self):
        application.quit()

    def construct_table(self, type):
        header_row = []
        header_id = 0
        idx_tab = 0
        tab_description = ''

        if type == 'FULL' :
            idx_tab = 0
            tab_description = self.tab_full
            headers = ['ID', 'NAME', 'GENRE', 'RATING', 'TYPE']
            self.tab_full_table = QTableWidget()
            self.tab_full_table.setColumnCount(len(headers))
            for h in headers:
                header_row.append(self.tab_full_table.setHorizontalHeaderItem(header_id, QTableWidgetItem(h)))
                header_id += 1
            if len(self.record_list) > 0:
                for row_i, single_data in enumerate(self.record_list):
                    self.tab_full_table.setRowCount(self.tab_full_table.rowCount()+1)
                    self.tab_full_table.setRowHeight(self.tab_full_table.rowCount()-1, 30)
                    id = QTableWidgetItem(str(single_data.id))
                    self.tab_full_table.setItem(row_i, 0, id)
                    name = QTableWidgetItem(single_data.name)
                    self.tab_full_table.setItem(row_i, 1, name)
                    genre = QTableWidgetItem(str(single_data.genre))
                    self.tab_full_table.setItem(row_i, 2, genre)
                    rating = QTableWidgetItem(single_data.rating)
                    self.tab_full_table.setItem(row_i, 3, rating)
                    type = QTableWidgetItem(str(single_data.type))
                    self.tab_full_table.setItem(row_i, 4, type)

            if len(self.record_list) > 0 or self.is_construct == False:
                self.tab.removeTab(idx_tab)
                self.tab.insertTab(idx_tab, self.tab_full_table, tab_description)
            else:
                self.tab.addTab(self.tab_full_table, self.tab_full)

            self.tab.setCurrentIndex(idx_tab)

        elif type == 'NAME':
            idx_tab = 1
            tab_description = self.tab_name
            headers = ['ID', 'NAME']            
            self.tab_name_table = QTableWidget()
            self.tab_name_table.setColumnCount(len(headers))
            for h in headers:
                header_row.append(self.tab_name_table.setHorizontalHeaderItem(header_id, QTableWidgetItem(h)))
                header_id += 1

            if len(self.record_list) > 0:
                for row_i, single_data in enumerate(self.record_list):
                    self.tab_name_table.setRowCount(self.tab_name_table.rowCount()+1)
                    self.tab_name_table.setRowHeight(self.tab_name_table.rowCount()-1, 30)
                    id = QTableWidgetItem(str(single_data.id))
                    self.tab_name_table.setItem(row_i, 0, id)
                    name = QTableWidgetItem(single_data.name)
                    self.tab_name_table.setItem(row_i, 1, name)

            if self.is_construct == False:
                self.tab.removeTab(idx_tab)
                self.tab.insertTab(idx_tab, self.tab_name_table, tab_description)
            else:
                self.tab.addTab(self.tab_name_table, self.tab_name)

            self.tab.setCurrentIndex(idx_tab)

        elif type == 'TYPE':
            idx_tab = 2
            tab_description = self.tab_type
            headers = ['ID', 'NAME', 'GENRE', 'RATING', 'TYPE']
            self.tab_type_table = QTableWidget()
            self.tab_type_table.setColumnCount(len(headers))
            for h in headers:
                header_row.append(self.tab_type_table.setHorizontalHeaderItem(header_id, QTableWidgetItem(h)))
                header_id += 1
            
            if len(self.record_list) > 0:
                for row_i, single_data in enumerate(self.record_list):
                    self.tab_type_table.setRowCount(self.tab_type_table.rowCount()+1)
                    self.tab_type_table.setRowHeight(self.tab_type_table.rowCount()-1, 30)
                    id = QTableWidgetItem(str(single_data.id))
                    self.tab_type_table.setItem(row_i, 0, id)
                    name = QTableWidgetItem(single_data.name)
                    self.tab_type_table.setItem(row_i, 1, name)
                    genre = QTableWidgetItem(str(single_data.genre))
                    self.tab_type_table.setItem(row_i, 2, genre)
                    rating = QTableWidgetItem(single_data.rating)
                    self.tab_type_table.setItem(row_i, 3, rating)
                    type = QTableWidgetItem(str(single_data.type))
                    self.tab_type_table.setItem(row_i, 4, type)

            if self.is_construct == False:
                self.tab.removeTab(idx_tab)
                self.tab.insertTab(idx_tab, self.tab_type_table, tab_description)
            else:
                self.tab.addTab(self.tab_type_table, self.tab_type)

            self.tab.setCurrentIndex(idx_tab)

        elif type == 'RATING':
            idx_tab = 3
            tab_description = self.tab_rating
            headers = ['ID', 'NAME', 'RATING']
            self.tab_rating_table = QTableWidget()
            self.tab_rating_table.setColumnCount(len(headers))
            for h in headers:
                header_row.append(self.tab_rating_table.setHorizontalHeaderItem(header_id, QTableWidgetItem(h)))
                header_id += 1

            if len(self.record_list) > 0:
                for row_i, single_data in enumerate(self.record_list):
                    self.tab_rating_table.setRowCount(self.tab_rating_table.rowCount()+1)
                    self.tab_rating_table.setRowHeight(self.tab_rating_table.rowCount()-1, 30)
                    id = QTableWidgetItem(str(single_data.id))
                    self.tab_rating_table.setItem(row_i, 0, id)
                    name = QTableWidgetItem(single_data.name)
                    self.tab_rating_table.setItem(row_i, 1, name)
                    rating = QTableWidgetItem(single_data.rating)
                    self.tab_rating_table.setItem(row_i, 2, rating)

            if self.is_construct == False:
                self.tab.removeTab(idx_tab)
                self.tab.insertTab(idx_tab, self.tab_rating_table, tab_description)
            else:
                self.tab.addTab(self.tab_rating_table, self.tab_rating)

            self.tab.setCurrentIndex(idx_tab)

        elif type == 'GENRE':
            idx_tab = 4
            tab_description = self.tab_genre
            headers = ['ID', 'NAME', 'GENRE']
            self.tab_genre_table = QTableWidget()
            self.tab_genre_table.setColumnCount(len(headers))
            for h in headers:
                header_row.append(self.tab_genre_table.setHorizontalHeaderItem(header_id, QTableWidgetItem(h)))
                header_id += 1

            if len(self.record_list) > 0:
                for row_i, single_data in enumerate(self.record_list):
                    self.tab_genre_table.setRowCount(self.tab_genre_table.rowCount()+1)
                    self.tab_rating_table.setRowHeight(self.tab_genre_table.rowCount()-1, 30)
                    id = QTableWidgetItem(str(single_data.id))
                    self.tab_genre_table.setItem(row_i, 0, id)
                    name = QTableWidgetItem(single_data.name)
                    self.tab_genre_table.setItem(row_i, 1, name)
                    genre = QTableWidgetItem(single_data.genre)
                    self.tab_genre_table.setItem(row_i, 2, genre)

            if self.is_construct == False:
                self.tab.removeTab(idx_tab)
                self.tab.insertTab(idx_tab, self.tab_genre_table, tab_description)
            else:
                self.tab.addTab(self.tab_genre_table, self.tab_genre)

            self.tab.setCurrentIndex(idx_tab)

if __name__ == '__main__':
    pyqt = os.path.dirname(PyQt6.__file__)
    QApplication.addLibraryPath(os.path.join(pyqt, "Qt", "plugins"))
    application = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(application.exec())