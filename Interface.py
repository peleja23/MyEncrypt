import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QInputDialog, QFileDialog
from PyQt5 import QtCore, QtGui, QtWidgets

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(700, 300, 510, 500)
        self.button_En = QPushButton("Encrypt", self)
        self.button_De = QPushButton("Decrypt", self)
        self.button_File = QPushButton("File", self)
        self.button_Folder = QPushButton("Folder", self)
        self.button_pass = QPushButton("Insert Password", self)
        self.button_ok = QPushButton("Ok", self)
        self.initUI()

        self.mode = None
        self.target_path = None
        self.password = None
        self.filter = None

    def initUI(self):
        self.button_En.setGeometry(100, 100, 100, 50)
        self.button_En.setStyleSheet("font-size: 20px;")
        self.button_En.clicked.connect(lambda: self.setMode("encrypt"))

        self.button_De.setGeometry(300, 100, 100, 50)
        self.button_De.setStyleSheet("font-size: 20px;")
        self.button_De.clicked.connect(lambda: self.setMode("decrypt"))

        self.le = QLabel(self)
        self.le.move(205, 62)
        self.le.setStyleSheet("font-size: 20px;")
        self.le.resize(100,22)

        self.button_File.setGeometry(100, 200, 100, 50)
        self.button_File.setStyleSheet("font-size: 20px;")
        self.button_File.clicked.connect(self.selectFile)

        self.button_Folder.setGeometry(300, 200, 100, 50)
        self.button_Folder.setStyleSheet("font-size: 20px;")
        self.button_Folder.clicked.connect(self.selectFolder)

        self.button_pass.setGeometry(175, 300, 160, 50)  
        self.button_pass.setStyleSheet("font-size: 20px;")
        self.button_pass.clicked.connect(self.showPasswordInsert) 

        self.button_ok.setGeometry(350, 400, 50, 50)  
        self.button_ok.setStyleSheet("font-size: 20px;")
        self.button_ok.clicked.connect(self.execute)  

        self.show()

    def setMode(self, mode):
        self.mode = mode
        print(f"Mode selected: {mode}")
        if mode == "encrypt":
            self.button_En.setDisabled(True)
            self.button_De.setDisabled(False)
            self.le.setText("Encription")
        if mode == "decrypt":
            self.button_De.setDisabled(True)
            self.button_En.setDisabled(False)
            self.le.setText("Decription")

    def selectFolder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:  
            print(f"Selected Folder: {folder_path}")
            self.button_Folder.setDisabled(True)
            self.button_File.setDisabled(True)
            filter, ok = QInputDialog.getText(self, 'Filter', 'Enter filter:')
            if ok:
                if not filter:
                    filter = 0
                print(filter)
        return folder_path, filter

    def selectFile(self):
        files = []
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*);;Text Files (*.txt);;Images (*.png *.jpg *.jpeg)")
        if file_path:
            print(f"Selected File: {file_path}")
            files.append(file_path)
        return files
    
    def showPasswordInsert(self):
        password, ok = QInputDialog.getText(self, 'Password', 'Enter text:')
        if ok:
            print(password)
            self.password = password
    
    def execute(self):
        if self.mode is None:
            print("Error: No mode selected (Encrypt or Decrypt)")
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('No mode selected!')
            return

        if self.password is None:
            print("Error: No password entered")
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('No password inserted!')
            return
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())