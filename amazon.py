#encoding:utf-8
from PyQt5.QtCore import QRect

WIDTH = 1200
HEIGHT = 1000

import sys
from Chess import RECT,BORDER
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLCDNumber
from PyQt5.QtGui import QPainter, QColor, QFont

from Game import Game


class Drawing(QWidget):
    def __init__(self,parent=None):
        super(Drawing,self).__init__(parent)
        self.initUI()


    def initUI(self):
        self.lcd = QLCDNumber(self)
        self.game=Game(self,self.lcd)
        self.resize(WIDTH, HEIGHT)  # 固定大小
        self.setMinimumSize(QtCore.QSize(WIDTH, HEIGHT))
        self.setMaximumSize(QtCore.QSize(WIDTH, HEIGHT))
        self.setWindowTitle("Amazons")  # 窗口名称
        self.ininFunction()
        self.show()



    def paintEvent(self, e):#绘制棋盘
        qp=QPainter()
        qp.begin(self)
        col = QColor(0, 0, 0)
        col.setNamedColor('#d4d4d4')
        qp.setPen(col)
        off = True
        for i in range(0, 10):
            for j in range(0, 10):
                if (off):
                    off = False
                    qp.setBrush(QColor(236, 207, 152))
                    qp.drawRect(i * RECT + BORDER,
                                j * RECT + BORDER, RECT,
                                RECT)
                else:
                    off = True
                    qp.setBrush(QColor(131, 67, 47))
                    qp.drawRect(i * RECT + BORDER,
                                j * RECT + BORDER, RECT,
                                RECT)
            if (off):
                off = False
            else:
                off=True
        qp.end()
    def ininFunction(self):
        self.startButton = QPushButton('Button', self)
        self.startButton.setText("开始游戏")
        self.startButton.resize(self.startButton.sizeHint())
        self.startButton.setGeometry(QtCore.QRect(950 , 150,150, 60))
        self.startButton.setFont(QFont("微软雅黑", 15, QFont.Bold))
        self.startButton.clicked.connect(self.startButtonClick)

        self.restartButton = QPushButton('Button', self)
        self.restartButton.setText("重新开始")
        self.restartButton.resize(self.restartButton.sizeHint())
        self.restartButton.setGeometry(QtCore.QRect(950 , 250,150, 60))
        self.restartButton.setFont(QFont("微软雅黑", 15, QFont.Bold))
        self.restartButton.clicked.connect(self.restartButtonClick)

        self.retractButton = QPushButton('Button', self)
        self.retractButton.setText("悔棋")
        self.retractButton.resize(self.retractButton.sizeHint())
        self.retractButton.setGeometry(QtCore.QRect(950 , 350,150, 60))
        self.retractButton.setFont(QFont("微软雅黑", 15, QFont.Bold))
        self.retractButton.clicked.connect(self.retractButtonClick)
        
        self.lcd.setGeometry(QRect(330, 220, 200, 70))
        self.lcd.setFont(QFont("微软雅黑", 20, QFont.Bold))
        self.lcd.setGeometry(QtCore.QRect(400 , 20,200, 60))
        self.lcd.display("00:00")

    def startButtonClick(self):
        text=self.startButton.text().encode("utf-8")
        if(text=="开始游戏"):
            self.game.startGame()
            self.startButton.setText("暂停游戏")
        elif(text=="暂停游戏"):
            self.game.stopGame()
            self.startButton.setText("继续游戏")
        elif(text=="继续游戏"):
            self.startButton.setText("暂停游戏")
            self.game.keepGame()
    def restartButtonClick(self):
        self.game.restartGame()
        text = self.startButton.text().encode("utf-8")
        if (text == "暂停游戏" or text == "继续游戏"):
            self.startButton.setText("开始游戏")
    def retractButtonClick(self):
        self.game.retract()

    def mousePressEvent(self, QMouseEvent):
        x=(QMouseEvent.x() - BORDER )/RECT
        y=(QMouseEvent.y() - BORDER )/RECT
        if (x >= 10 or y >= 10 or x < 0 or y < 0):#越界
            return
        else:
            self.game.onClick(x,y)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Drawing()
    sys.exit(app.exec_())