import numpy as np
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QWidget, QComboBox, QTextEdit, QLineEdit, \
    QFileDialog
import sys
from main import Methods


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi("C:\\Users\\smart\\Desktop\\assignments\\New folder\\pythonProject3\\1.ui", self)

        self.choose_file = self.findChild(QPushButton, "choose_file")
        self.submit = self.findChild(QPushButton, "submit")

        self.method = self.findChild(QComboBox, "methodname")
        self.eq_num = self.findChild(QTextEdit, "nu_of_equations")
        self.percision = self.findChild(QTextEdit, "percision")
        self.it = self.findChild(QTextEdit, "iterations")
        self.init = self.findChild(QTextEdit, "init_values")
        self.answer=self.findChild(QLabel, "answer")

        self.eq1 = self.findChild(QLineEdit, "eq1")
        self.eq2 = self.findChild(QLineEdit, "eq2")
        self.eq3 = self.findChild(QLineEdit, "eq3")
        self.eq4 = self.findChild(QLineEdit, "eq4")
        self.eq5 = self.findChild(QLineEdit, "eq5")
        # self.eq6 = self.findChild(QLineEdit, "eq6")
        # self.eq7 = self.findChild(QLineEdit, "eq7")
        # self.eq8 = self.findChild(QLineEdit, "eq8")
        # self.eq9 = self.findChild(QLineEdit, "eq9")
        # self.eq10 = self.findChild(QLineEdit, "eq10")

        self.choose_file.clicked.connect(self.clicker)
        self.submit.clicked.connect(self.clicker1)

        self.qle_list = []
        self.qle_list.append(self.eq1)
        self.qle_list.append(self.eq2)
        self.qle_list.append(self.eq3)
        self.qle_list.append(self.eq4)
        self.qle_list.append(self.eq5)
        # self.qle_list.append(self.eq6)
        # self.qle_list.append(self.eq7)
        # self.qle_list.append(self.eq8)
        # self.qle_list.append(self.eq9)
        # self.qle_list.append(self.eq10)
        self.show()

    def clicker(self):
        fname = QFileDialog().getOpenFileName(self, "Open File",
                                              "C:\\Users\\smart\\Desktop\\assignments\\New folder\\pythonProject3",
                                              "Text Files (*.txt)")[0]
        if fname:
            file1 = open(fname, 'r')

            QTextEdit(self.eq_num.setText(file1.readline().rstrip()))
            QComboBox(self.method.setCurrentText(file1.readline().rstrip()))

            for i in range(int(self.eq_num.toPlainText())):
                QLineEdit(self.qle_list[i].setText(file1.readline()))

            m = str(self.method.currentText())
            if m == "Gauss-seidel":
                QTextEdit(self.init.setText(file1.readline().rstrip()))

    def clicker1(self):

        #ARRAY OF EQUATIONS
        A = []
        #INITIAL VALUES
        X = []
        #NO OF EQUATIONS
        n = int(self.eq_num.toPlainText())

        for i in range(n):
            A.append(self.qle_list[i].text().rstrip())

        m = str(self.method.currentText())
        init = str(self.init.toPlainText())
        if m == "Gauss-seidel":
            for i in init.split(sep=' '):
                X.append(float(i))

        es=float(self.percision.toPlainText())
        max_iterations=int(self.it.toPlainText())
        #print("Array of equations : ")
        #print(A)
        #print("Array of init_vals : ")
        #print(X)
        #print("NU_OF_EQ : ")
        #print(n)
        #print("method : ")
        #print(m)
        #print("Percision : ")
        #print(es)
        #print("Max It : ")
        #print(max_iterations)
        if m == "Gauss-elimination":
            my_method = Methods(n,es,max_iterations,A)
            my_method.gauss_elimination()
            print(my_method.solutions)

        elif m == "Lu-decomposition":
            my_method = Methods(n,es,max_iterations,A)
            my_method.lu_decomposition()
            print(my_method.solutions)
        elif m == "Gauss-jordan":
            my_method = Methods(n,es,max_iterations,A)
            my_method.gauss_jordan()

        elif m == "Gauss-seidel":
            my_method = Methods(n,es,max_iterations,A,X)
            my_method.gauss_seidel()

        QLabel(self.answer.setText(str(my_method.solutions)))

app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
#3x+2y+1z-6b
#2x+3y+0z-7b
#0x+0y+2z-4b
