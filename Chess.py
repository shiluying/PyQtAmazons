# -*- coding:utf-8 -*-
from PyQt5.QtGui import QColor, QPixmap
RECT=80
BORDER=100
from PyQt5.QtWidgets import QLabel

class LaBel(QLabel):
    def __init__(self, parent):
        super(LaBel,self).__init__(parent)
        self.setMouseTracking(True)

    def enterEvent(self, e):
        e.ignore()

class Obstacle():
    def __init__(self,x,y,wd):
        self.x=x
        self.y=y
        self.wd=wd
        self.obstacle=QPixmap('img/ob.png')
        self.init()
    def init(self):
        self.piece = LaBel(self.wd)
        self.piece.setVisible(True)  # 图片可视
        self.piece.setScaledContents(True)  # 图片大小根据标签大小可变
        self.piece.setPixmap(self.obstacle)
        self.piece.setGeometry(self.x * RECT + BORDER,
                                self.y * RECT + BORDER, RECT, RECT )
    def draw(self):
        self.piece.setGeometry(self.x * RECT + BORDER,
                               self.y * RECT + BORDER, RECT, RECT)

class Chess():
    def __init__(self,type,x,y,id):
        self.type=type
        self.x=x
        self.y=y
        self.id=id
        self.obstacle=[]
        self.piece=LaBel
    def addObstacle(self,ob):
        self.obstacle.append(ob)
    def removeObstacle(self):
        return self.obstacle.pop()
    def changePostion(self,x,y):
        self.x=x
        self.y=y
        self.draw()
    def draw(self):
        self.piece.setGeometry(self.x * RECT + BORDER,
                               self.y * RECT + BORDER , RECT-3, RECT-3)
    def drawSelect(self):
        self.piece.setGeometry(self.x * RECT + BORDER,
                                self.y * RECT + BORDER, RECT+3, RECT+3)

