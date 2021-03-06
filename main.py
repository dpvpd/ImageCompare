# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
import os
import sys
from selectfolder import Select
from PRGRMINFO import ProgramInfo
from DEVINFO import DevInfo

dir = os.getcwd() + '\\data\\'
_translate = QtCore.QCoreApplication.translate
ui = uic.loadUiType(dir+'main.ui')[0]
isfullscreen = False

class Form(QtWidgets.QMainWindow, ui):
    def __init__(self):
        super().__init__()
        self.index = 0
        self.setupUi(self)
        self.action.triggered.connect(self.runSelectDir)
        self.action_2.triggered.connect(self.programInfo)
        self.action_3.triggered.connect(self.devloperInfo)
        self.pushButton.clicked.connect(self.rightButton)
        self.pushButton_2.clicked.connect(self.leftButton)
        #self.listWidget.dropped.connect(lambda:print("!!"))
        self.listWidget.model().rowsMoved.connect(self.moved1)
        self.listWidget_2.model().rowsMoved.connect(self.moved2)
        self.show()
    
    def runSelectDir(self):
        select = Select()
        r = select.showModal()
        if r:
            path1 = select.lineEdit.text()
            path2 = select.lineEdit_2.text()
            if select.radioButton.isChecked():
                ext = 0
            elif select.radioButton_2.isChecked():
                ext = 1
            if path1!='' and path2!='':
                self.loadDirs(path1, path2, ext)
            else:
                QtWidgets.QMessageBox.critical(self,'경로 입력되지 않음','폴더 경로 두개 중 한개 이상이 입력되지 않았습니다.',QtWidgets.QMessageBox.Yes,QtWidgets.QMessageBox.Yes)
        return
    def loadDirs(self,path1,path2,ext):
        self.path1 = path1
        self.path2 = path2
        self.ext = ext
        try:
            if ext==1:
                self.dirList1 = [file for file in os.listdir(path1) if file.endswith('.jpg')]
                self.dirList2 = [file for file in os.listdir(path2) if file.endswith('.jpg')]
            elif ext==0:
                self.dirList1 = [file for file in os.listdir(path1) if file.endswith('.png')]
                self.dirList2 = [file for file in os.listdir(path2) if file.endswith('.png')]
        except:
            QtWidgets.QMessageBox.critical(self,'경로 잘못됨','입력된 경로가 잘못되었습니다. \n존재하지 않거나 불러올 수 없는 폴더입니다.',QtWidgets.QMessageBox.Yes,QtWidgets.QMessageBox.Yes)
            return
        b = set(self.dirList1)
        self.dirList1_ = list(b)
        c = set(self.dirList2)
        self.dirList2_ = list(c)

        self.dirList = self.dirList1
        self.dirList.extend(self.dirList2)
        a = set(self.dirList)
        self.dirList = list(a)
        self.dirList.sort()
        self.dirList1_.sort()
        self.dirList2_.sort()
        
        self.dirList1 = []
        self.dirList2 = []
        i = 0
        j1 = 0
        j2 = 0
        while i<len(self.dirList):
            if j1>=len(self.dirList) or j2>=len(self.dirList):
                break
            if self.dirList[i]==self.dirList1_[j1]:
                self.dirList1.append(self.dirList1_[j1])
                j1+=1
                if j1 >= len(self.dirList1_):
                    j1-=1
            else:
                self.dirList1.append('')
            if self.dirList[i]==self.dirList2_[j2]:
                self.dirList2.append(self.dirList2_[j2])
                j2+=1
                if j2 >= len(self.dirList2_):
                    j2-=1
            else:
                self.dirList2.append('')
            i+=1
        self.listWidget.clear()
        self.listWidget_2.clear()
        for i in self.dirList1:
            self.listWidget.addItem(i)
        for i in self.dirList2:
            self.listWidget_2.addItem(i)
        self.index=0
        self.imagePrinter()

    def keyPressEvent(self, e):
        global isfullscreen
        if e.key() == Qt.Key_Escape:
            self.close()
        elif e.key() == Qt.Key_F:
            isfullscreen=not isfullscreen
            if isfullscreen:
                self.showFullScreen()
            else:
                self.showNormal()
        if e.key() == Qt.Key_Left:
            self.index -= 1
            self.imagePrinter()
        elif e.key() == Qt.Key_Right:
            self.index += 1
            self.imagePrinter()
        elif e.key() == Qt.Key_Up:
            self.index -= 1
            self.imagePrinter()
        elif e.key() == Qt.Key_Down:
            self.index += 1
            self.imagePrinter()
    
    def imagePrinter(self):
        if self.index >= len(self.dirList):
            self.index -= len(self.dirList)
        if self.dirList1[self.index] != '':
            imagefile1 = self.path1+self.dirList1[self.index]
            self.label.setPixmap(QtGui.QPixmap(imagefile1))
        else:
            self.label.setPixmap(QtGui.QPixmap(dir+'404.png'))
        if self.dirList2[self.index] != '':
            imagefile2 = self.path2+self.dirList2[self.index]
            self.label_2.setPixmap(QtGui.QPixmap(imagefile2))
        else:
            self.label.setPixmap(QtGui.QPixmap(dir+'404.png'))
        self.statusBar.showMessage('현재 파일 : '+self.dirList[self.index])
    
    def programInfo(self):
        pinfo = ProgramInfo()
        a = pinfo.showModal()
        return
    def devloperInfo(self):
        dinfo = DevInfo()
        a = dinfo.showModal()
        return
    def rightButton(self):
        self.index+=1
        self.imagePrinter()
    def leftButton(self):
        self.index-=1
        self.imagePrinter()

    def moved1(self):
        changed = []
        for i in range(self.listWidget.count()):
            changed.append(self.listWidget.item(i).text())
        if len(self.dirList1) != len(changed):
            QtWidgets.QMessageBox.critical(self,'잘못된 이동','옆 리스트로 옮기면 프로그램이 뻗습니다.',QtWidgets.QMessageBox.Yes,QtWidgets.QMessageBox.Yes)
            QtWidgets.QMessageBox.information(self,'개발자의 양심고백','사실 원래라면 뻗을지 어떨지는 모르겠지만\n어찌될지 모르겠어서 그냥 뻗게 했습니다.',QtWidgets.QMessageBox.Yes,QtWidgets.QMessageBox.Yes)
            exit(0)
        i = 0
        c = []
        while i<len(self.dirList1):
            if changed[i] != self.dirList1[i] and changed[i] != '':
                os.rename(self.path1 + changed[i], self.path1 + self.dirList[i]+'tmp')
                c.append(self.dirList[i]+'tmp')
                #이름 예시 : 0001.jpg -> 0002.jpgtmp
            i+=1
        for j in c:
            os.rename(self.path1+j, self.path1+j[:-3])
        self.loadDirs(self.path1, self.path2, self.ext)
        return
    def moved2(self):
        changed = []
        for i in range(self.listWidget_2.count()):
            changed.append(self.listWidget_2.item(i).text())
        if len(self.dirList2) != len(changed):
            QtWidgets.QMessageBox.critical(self,'잘못된 이동','옆 리스트로 옮기면 프로그램이 뻗습니다.',QtWidgets.QMessageBox.Yes,QtWidgets.QMessageBox.Yes)
            QtWidgets.QMessageBox.information(self,'개발자의 양심고백','사실 원래라면 뻗을지 어떨지는 모르겠지만\n어찌될지 모르겠어서 그냥 뻗게 했습니다.',QtWidgets.QMessageBox.Yes,QtWidgets.QMessageBox.Yes)
            exit(0)
        i = 0
        c = []
        while i<len(self.dirList2):
            if changed[i] != self.dirList2[i] and changed[i] != '':
                os.rename(self.path2 + changed[i], self.path2 + self.dirList[i]+'tmp')
                c.append(self.dirList[i]+'tmp')
                #이름 예시 : 0001.jpg -> 0002.jpgtmp
            i+=1
        for j in c:
            os.rename(self.path2+j, self.path2+j[:-3])
        self.loadDirs(self.path1, self.path2, self.ext)
        return


if __name__ == '__main__':
    app=QtWidgets.QApplication(sys.argv)
    form = Form()
    sys.exit(app.exec_())