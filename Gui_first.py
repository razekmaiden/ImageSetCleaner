import sys
import os
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, QScrollArea, QAction, QMainWindow


# https://stackoverflow.com/questions/3157766/how-can-i-achieve-layout-similar-to-google-image-search-in-qt-pyqt/3160725
# https://stackoverflow.com/questions/38223705/adding-items-from-a-text-file-to-qlistwidget-in-pyqt5
# http://pythoncentral.io/pyside-pyqt-tutorial-the-qlistwidget/
# http://pythoncentral.io/pyside-pyqt-tutorial-qlistview-and-qstandarditemmodel/
# https://stackoverflow.com/questions/46493125/pyqt-change-picture-with-keyboard-button

# TODO: Watch this
# https://stackoverflow.com/questions/8814452/pyqt-how-to-add-separate-ui-widget-to-qmainwindow

class MainWindow(QMainWindow):
    def __init__(self, paths, parent=None):
        super(MainWindow, self).__init__(parent)
        self.window = Window(paths)

        deleteAct = QAction(QIcon('./Resource/trash_icon.png'), 'Delete Selection', self)
        deleteAct.setStatusTip('Will delete the selected images')
        deleteAct.triggered.connect(self.delete_images)
        # exitAct.triggered.connect(qApp.quit)


        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(deleteAct)

        self.setCentralWidget(self.window)

        self.show()

    def delete_images(self):
        print(self.window.get_selection())


class ClikableLabel(QLabel):

    def __init__(self, path):
        super(ClikableLabel, self).__init__()
        self.width = 180
        self.height = 200
        self.isChecked = False

        pixmap = QPixmap(path)
        pixmap = pixmap.scaled(self.width, self.height, QtCore.Qt.KeepAspectRatio)
        self.setPixmap(pixmap)

    def mousePressEvent(self, event):
        self.isChecked = not self.isChecked

        if self.isChecked:
            self.setStyleSheet("border: 5px inset red;")
        else:
            self.setStyleSheet("")


class Window(QScrollArea):
    def __init__(self, paths):
        QScrollArea.__init__(self)

        # scroll = QScrollArea()
        # scroll.setWidgetResizable(True)
        # scroll.setFixedHeight(400)
        widget = QWidget()
        self.layout = QGridLayout(widget)
        self.paths = paths
        self.all_labels = []
        self.nb_columns = 5

        self.populate_grid(self.paths)



        self.setWidget(widget)

        self.setWidgetResizable(True)
        self.setMinimumWidth(1000)
        self.setMinimumHeight(600)

    def populate_grid(self, paths):
        row = 0
        column = 0
        for idx, path in enumerate(paths):
            label = ClikableLabel(path)
            self.all_labels.append(label)
            self.layout.addWidget(self.all_labels[idx], row, column)

            column += 1
            if column % self.nb_columns == 0:
                row += 1
                column = 0

    def get_selection(self):
        selection = []
        for idx, path in enumerate(self.paths):
            if self.all_labels[idx].isChecked:
                selection.append(path)

        return selection



if __name__ == '__main__':

    img_list = ['./Test_cluster_1/img01.jpg', './Test_cluster_1/img02.jpg']
    path = './Test_cluster_1/'
    images = os.listdir(path)
    img_list = [os.path.join(path, image) for image in images]

    app = QApplication(sys.argv)
    window = MainWindow(img_list)
    # window.setGeometry(500, 300, 200, 200)
    # window.show()
    sys.exit(app.exec_())