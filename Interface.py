import sys
import subprocess
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QInputDialog, QFileDialog, QMessageBox

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(700, 300, 510, 500)
        self.setWindowTitle("My Encrypter")
        self.setWindowIcon(QIcon("icon.png"))
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
        self.flag = None #0 if file and 1 if folder

    def initUI(self):
        self.button_En.setGeometry(100, 100, 100, 50)
        self.button_En.setStyleSheet("""QPushButton {font-size: 20px; background-color: gray; color: yellow;border-radius: 5px; border: 2px solid rgb(10, 10, 10);}
                                    QPushButton:disabled {font-size: 20px;background-color: rgb(37, 161, 144);color: yellow;border-radius: 5px;border: 2px solid rgb(10, 10, 10);}
                                     """)
        self.button_En.clicked.connect(lambda: self.setMode("encrypt"))

        self.button_De.setGeometry(300, 100, 100, 50)
        self.button_De.setStyleSheet("""QPushButton {font-size: 20px; background-color: gray; color: yellow;border-radius: 5px; border: 2px solid rgb(10, 10, 10);}
                                    QPushButton:disabled {font-size: 20px;background-color: rgb(37, 161, 144);color: yellow;border-radius: 5px;border: 2px solid rgb(10, 10, 10);}
                                     """)
        self.button_De.clicked.connect(lambda: self.setMode("decrypt"))

        self.button_File.setGeometry(100, 200, 100, 50)
        self.button_File.setStyleSheet("font-size: 20px; background-color: rgb(37, 161, 144); color: yellow;border-radius: 5px; border: 2px solid rgb(10, 10, 10);")
        self.button_File.clicked.connect(self.selectFile)

        self.button_Folder.setGeometry(300, 200, 100, 50)
        self.button_Folder.setStyleSheet("font-size: 20px; background-color: rgb(37, 161, 144); color: yellow;border-radius: 5px; border: 2px solid rgb(10, 10, 10);")
        self.button_Folder.clicked.connect(self.selectFolder)

        self.button_pass.setGeometry(175, 300, 160, 50)  
        self.button_pass.setStyleSheet("font-size: 20px; background-color: rgb(37, 161, 144); color: yellow;border-radius: 5px; border: 2px solid rgb(10, 10, 10);")
        self.button_pass.clicked.connect(self.showPasswordInsert) 

        self.button_ok.setGeometry(350, 400, 50, 50)  
        self.button_ok.setStyleSheet("font-size: 20px; background-color: rgb(37, 161, 144); color: yellow;border-radius: 5px; border: 2px solid rgb(10, 10, 10);")
        self.button_ok.clicked.connect(self.execute)  

        self.select_mode = QLabel(self)
        self.select_mode.move(190, 62)
        self.select_mode.setStyleSheet("font-size: 20px;border-radius: 5px")
        self.select_mode.resize(150,22)

        self.select_path = QLabel(self)
        self.select_path.move(65, 262)
        self.select_path.setStyleSheet("font-size: 15px;border-radius: 5px")
        self.select_path.resize(1000,22)

        self.show()

    def setMode(self, mode):
        self.mode = mode
        print(f"Mode selected: {mode}")

        if mode == "encrypt":
            self.button_En.setDisabled(True)
            self.button_De.setDisabled(False)
            self.select_mode.setText("⚠️Encription")

        if mode == "decrypt":
            self.button_De.setDisabled(True)
            self.button_En.setDisabled(False)
            self.select_mode.setText("⚠️Decription")

    def selectFolder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:  
            print(f"Selected Folder: {folder_path}")
            filter, ok = QInputDialog.getText(self, 'Filter', 'Enter filter:')
            if ok:
                if not filter:
                    self.filter = 0
                print(filter)
                self.filter = filter
            self.select_path.setText(f"📁->{folder_path}/{filter}")
            self.target_path = folder_path
            self.flag = 1

    def selectFile(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*);;Text Files (*.txt);;Images (*.png *.jpg *.jpeg)")
        if file_path:
            print(f"Selected File: {file_path}")
            self.select_path.setText(f"📄->{file_path}")
            self.target_path = file_path
            self.flag = 0
    
    def showPasswordInsert(self):
        password, ok = QInputDialog.getText(self, 'Password', 'Enter Password:')
        if ok:
            print(password)
            self.password = password
    
    def execute(self):
        if self.mode is None:
            print("Error: No mode selected (Encrypt or Decrypt)")
            error = QMessageBox()
            error.setIcon(QMessageBox.Critical)
            error.setText("Error")
            error.setInformativeText('Missing Mode')
            error.setWindowTitle("Error")
            error.exec_()

        if self.password is None:
            print("Error: No password entered")
            error = QMessageBox()
            error.setIcon(QMessageBox.Critical)
            error.setText("Error")
            error.setInformativeText('Missing Password')
            error.setWindowTitle("Error")
            error.exec_()

        if self.target_path is None:
            print("Error: No path defined")
            error = QMessageBox()
            error.setIcon(QMessageBox.Critical)
            error.setText("Error")
            error.setInformativeText('Missing path')
            error.setWindowTitle("Error")
            error.exec_()

        elif self.flag == 0:
            try:
                subprocess.run(["python3", "FileSafety.py", self.mode, self.password, self.target_path, self.target_path])
            except subprocess.CalledProcessError:
                print(f"Execution failed")
            return
        
        elif self.flag == 1:
            try:
                subprocess.run(["python3", "FolderSafety.py", self.mode, self.password, self.target_path, self.filter])
            except subprocess.CalledProcessError:
                print(f"Execution failed")
            return
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    palette = QPalette()
    palette.setColor(QPalette.ButtonText, QColor(37, 161, 144))
    app.setPalette(palette)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())