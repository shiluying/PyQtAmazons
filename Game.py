# -*- coding:utf-8 -*-
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMessageBox

from sqlalchemy import false, true

from Chess import *
from PyQt5.QtGui import QPixmap


class Game():
    def __init__(self,wd,lcd):
        self.wd = wd
        self.lcd=lcd
    def init(self):
        self.chesses = []
        self.board = [[-1 for n in range(10)] for m in range(10)]
        self.boards = []
        self.black = QPixmap('img/black.png')
        self.white = QPixmap('img/white.png')
        self.StartFlag = false
        self.second = 0
        self.minute=0
        self.timer=QTimer()
        self.timer.timeout.connect(self.changeTime)
        self.alreadyMove = false
        self.lastChess = None
        self.player = "BLACK"  # 当前走子玩家
        self.localPlayer = "BLACK"  # 选择的颜色

    def initChess(self):
        for i in range(0,4):
            if(i<2):
                self.chesses.append(Chess("BLACK",i*3+3,0,i))
                self.board[i * 3+3][0]=i
            else:
                self.chesses.append(Chess("BLACK", (i-2) * 9, 3, i))
                self.board[(i - 2) * 9][3] = i
        for i in range(0,4):
            if(i<2):
                self.chesses.append(Chess("WHITE",i*9,6,i+4))
                self.board[i*9][6]=i+4
            else:
                self.chesses.append(Chess("WHITE", (i-1) * 3, 9, i+4))
                self.board[(i-1)*3][9]=i+4
        for chess in self.chesses:
            chess.piece = LaBel(self.wd)
            chess.piece.setVisible(True)  # 图片可视
            chess.piece.setScaledContents(True)  # 图片大小根据标签大小可变
            if (chess.type == "WHITE"):
                chess.piece.setPixmap(self.white)  # 放置白色棋子
            else:
                chess.piece.setPixmap(self.black)
            chess.piece.setGeometry(chess.x * RECT + BORDER,
                                        chess.y * RECT + BORDER, RECT-3, RECT-3)

    def drawChesses(self,qp):
        for chess in self.chesses:
            chess.drawChess(qp)
            chess.drawObstacle(qp)
    def reversePlayer(self):
        if(self.player=="WHITE"):
            self.player="BLACK"
        else:
            self.player="WHITE"
    def addBoard(self):
        b = [[-1 for n in range(10)] for m in range(10)]
        for i in range(0,10):
            for j in range(0,10):
                b[i][j]=self.board[i][j]
        self.boards.append(b)
    def startGame(self):
        self.init()
        # 选择先后手
        reply = QMessageBox.question(self.wd, "请选择你所执子的颜色", "黑子为先手，白子为后手，AI将选择与你相反的颜色。是否选择黑子为先手？",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if (reply == QMessageBox.No):
            self.localPlayer="WHITE"
        self.initChess()
        self.addBoard()
        self.StartFlag=true
        self.timer.start(1000)
        print "Start Game"
    def restartGame(self):
        for chess in self.chesses:
            chess.piece.setVisible(False)
            for ob in chess.obstacle:
                ob.piece.setVisible(False)
            chess.obstacle=[]
        self.StartFlag = false
        self.lcd.display("00:00")

    def stopGame(self):
        self.StartFlag=false
        print "Stop Game"
    def keepGame(self):
        self.StartFlag = true
        print "Keep Game"
    def gameOver(self,winner):#未判断条件
        self.StartFlag=false
        print "Game Over"
        if winner == self.localPlayer:
            reply = QMessageBox.question(self.wd, 'You Win!', 'Continue?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        else:
            reply = QMessageBox.question(self.wd, 'You Lost!', 'Continue?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:  # 复位
            self.restartGame()
    def retract(self):
        if(self.StartFlag==false or self.boards.__len__()==1):
            return
        b=self.boards.pop()
        for i in range(0,10):
            for j in range(0,10):
                self.board[i][j]=self.boards[self.boards.__len__()-1][i][j]
                if(b[i][j]>-1):
                    c=self.chesses[b[i][j]]
                    if(c.x!=i or c.y!=j):#需要悔棋的棋子
                        c.changePostion(i,j)#移动位置
                        removeOb=c.removeObstacle()
                        removeOb.piece.setVisible(False)
                        for ob in c.obstacle:
                            ob.draw()
                        self.reversePlayer()
                        print "Retract Chess"
    def changeTime(self):
        if(self.StartFlag==false):
            return
        self.second=self.second+1
        if(self.second==60):
            self.second=0
            self.minute=self.minute+1
        self.lcd.display(self.checkTime())
    def checkTime(self):
        text=""
        if(self.second<10):
            text="0"+str(self.second)
        else:
            text=str(self.second)+""
        if(self.minute<10):
            text="0"+str(self.minute)+":"+text
        else:
            text=str(self.minute)+":"+text
        return text
    def onClick(self,x,y):
        if(self.StartFlag==false or self.localPlayer!=self.player):
            return
        id=self.board[x][y]
        if(id>=0 and self.alreadyMove==false):#选择棋子
            chess=self.chesses[id]
            if(chess.type==self.localPlayer):#己方棋子
                if(self.lastChess!=None):
                    self.lastChess.draw()
                chess.drawSelect()
                self.lastChess=chess
        elif(id==-1 and self.lastChess!=None and self.alreadyMove==false):#移动棋子
            self.lastChess.changePostion(x,y)
            self.board[x][y]=self.lastChess.id
            self.alreadyMove=true
        elif(id==-1 and self.alreadyMove==true):#选择完棋子，释放障碍
            ob=Obstacle(x,y,self.wd)
            self.lastChess.addObstacle(ob)
            self.board[x][y] = -2
            self.alreadyMove=false
            self.lastChess=None
            self.addBoard()
            self.reversePlayer()