import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from random import randint
import time

from PyQt5.uic.properties import QtGui


class Brag(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self)

        self.setWindowTitle('Brag!!')
        self.resize(600, 400)

        self.guess_view = QTextBrowser(self)
        self.guess_amount_box = QSpinBox(self)
        self.guess_number_box = QComboBox(self)
        self.win_hint = QLabel(self)
        self.my_dice_lb = QLabel(self)
        self.op_dice_lb = QLabel(self)

        self.guess_btn = QPushButton(self)
        self.start_btn = QPushButton(self)
        self.uncover = QPushButton(self)

        self.win_times = QLabel(self)
        self.literal_lb = QLabel(self)

        self.help_btn = QPushButton(self)

        self.my_dice = [0, 0, 0]
        self.op_dice = [0, 0, 0]

        # 最近一次的猜测(数组代表[0]个[1], 若[1]为不知道,则为0)
        self.my_guess = [0, 0]
        self.op_guess = [0, 0]

        self.initUi()

    def initUi(self):

        self.guess_view.resize(200, 230)
        self.guess_view.move(100, 30)

        self.guess_amount_box.resize(60, 30)
        self.guess_amount_box.move(220, 300)
        self.guess_amount_box.setRange(3, 6)
        self.guess_amount_box.setSingleStep(1)

        self.guess_number_box.resize(70, 30)
        self.guess_number_box.move(320, 300)
        self.guess_number_box.addItems(["2", "3", "4", "5", "6"])

        self.literal_lb.setText("个")
        self.literal_lb.move(290, 305)
        self.literal_lb.resize(20, 20)

        self.guess_btn.setText("吹牛")
        self.guess_btn.resize(100, 30)
        self.guess_btn.move(400, 350)
        self.guess_btn.clicked.connect(self.on_brag_btn)

        self.uncover.setText("揭了")
        self.uncover.resize(100, 30)
        self.uncover.move(250, 350)
        self.uncover.clicked.connect(self.on_uncover_btn)

        self.start_btn.setText("开始")
        self.start_btn.resize(100, 30)
        self.start_btn.move(100, 350)
        self.start_btn.clicked.connect(self.on_start_btn)

        self.my_dice_lb.setText("我的骰子:")
        self.my_dice_lb.resize(100, 30)
        self.my_dice_lb.move(400, 150)

        self.op_dice_lb.setText("对方骰子:")
        self.op_dice_lb.resize(100, 30)
        self.op_dice_lb.move(400, 100)

        self.win_hint.setText("")
        self.win_hint.resize(50, 30)
        self.win_hint.move(400, 200)

        self.help_btn.setText("帮助")
        self.help_btn.resize(100, 30)
        self.help_btn.move(480, 5)
        self.help_btn.clicked.connect(self.on_help_btn)

    def on_help_btn(self):
        QMessageBox.question(self, '帮助', '吹牛的具体规则请百度查询, 这里使用双方各3个骰子, 对手先手. 先点击<开始>, 摇骰子，然后左上角的'
                                         '文本框里就会有对手的猜测记录, 选择自己的猜测结果，点击<吹牛>进行猜测。点击<揭了>，游戏结束，公布结果。')

    def on_start_btn(self):
        self.guess_view.clear()
        self.op_dice_lb.clear()
        self.my_dice_lb.clear()
        self.win_hint.clear()
        self.my_guess = [0, 0]
        self.op_guess = [0, 0]
        self.op_dice = [0, 0, 0]
        self.my_dice = [0, 0, 0]

        self.my_dice = randint(1, 6), randint(1, 6), randint(1, 6)
        self.op_dice = randint(1, 6), randint(1, 6), randint(1, 6)
        while self.my_dice == [1, 2, 3]:  # 1,2,3 不吹牛
            self.my_dice = randint(1, 6), randint(1, 6), randint(1, 6)

        while self.op_dice == [1, 2, 3]:
            self.op_dice = randint(1, 6), randint(1, 6), randint(1, 6)
        self.my_dice_lb.setText("我的骰子: " + str(self.my_dice[0]) + ',' + str(self.my_dice[1]) + ',' + str(self.my_dice[2]))
        self.op_decide()

    def on_brag_btn(self):
        self.win_hint.clear()
        if self.my_dice == [0, 0, 0] or self.op_dice == [0, 0, 0]:
            self.win_hint.setText("请先点击开始")
            return
        g1 = int(self.guess_amount_box.value())
        g2 = int(self.guess_number_box.currentText())

        if g1 < self.op_guess[0]:
            self.win_hint.setText("规则错误，请重新选择数字")
            return
        if g1 == self.op_guess[0] and g2 <= self.op_guess[1]:  # 1 是最大的
            self.win_hint.setText("规则错误，请重新选择数字")
            return

        self.my_guess[0] = g1
        self.my_guess[1] = g2
        temp = "不知道" if self.my_guess[1] == 0 else str(self.my_guess[1])
        self.guess_view.append("我 " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\n" +
                               str(self.my_guess[0]) + "个" + temp)
        self.op_decide()

    def on_uncover_btn(self):
        total_list = self.op_dice + self.my_dice
        if total_list.count(self.op_guess[1]) + total_list.count(1) >= self.op_guess[0] and self.op_guess[1] != 1:
            self.win_hint.setText("你输了")
        elif self.op_guess[1] == 1 and total_list.count(1) >= self.op_guess[0]:
            self.win_hint.setText("你输了")
        else:
            self.win_hint.setText("你赢了")
        self.op_dice_lb.setText("对方骰子: " + str(self.op_dice[0]) + ',' + str(self.op_dice[1]) + ',' + str(self.op_dice[2]))

    def op_decide(self):
        c1 = self.op_dice.count(1)
        c2 = 0
        c3 = []
        c4 = 0
        for i in range(2, 7):
            if self.op_dice.count(i) == 2:
                c2 = i
            elif self.op_dice.count(i) == 3:
                c4 = i
            elif self.op_dice.count(i) == 1:
                c3.append(i)

        if self.op_guess[0] == 0:  # 第一次猜
            if c4 != 0:  # 有成三的, 猜3个不知道
                self.op_guess = [3, 0]
            elif c2 != 0:
                if c1 == 1:  # 有成双且有一个1的, 还是猜3个不知道
                    self.op_guess = [3, 0]
                else:         # 留底, 1/3 概率猜落单的那个
                    if randint(0, 2) == 0:
                        self.op_guess = [3, c3[0]]
                    else:
                        self.op_guess = [3, 0]
            elif c1 == 1:  # 有1个1
                if randint(0, 3) == 0:  # 铤而走险
                    ex_list = []
                    for i in range(2, 7):
                        if i not in c3:
                            ex_list.append(i)
                    self.op_guess = [3, ex_list[0]]
                else:
                    self.op_guess = [3, c3[0]]
            elif c1 == 2:  # 有两个1
                if randint(0, 2) == 0:  # 1/3 的概率3个不知道
                    self.op_guess = [3, 0]
                else:
                    k = c3[0]
                    if k > 2:    # 骗他一手
                        k -= 1
                    else:
                        k = 0
                    self.op_guess = [3, k]
            elif c1 == 3:  # 3个1, 随便猜, 但是不能猜3个不知道
                self.op_guess = [3, randint(2, 6)]
            else:  # 三个全单, 只能喊不知道
                self.op_guess = [3, 0]

        else:  # 不是第一轮吹牛(所以要关注它的上一轮猜测)
            #  由于玩家是第二轮, 因此不可能猜3个不知道
            weight = self.op_dice.count(self.my_guess[1])
            #  猜的个数为3的时候
            if self.my_guess[0] == 3:
                if weight == 0 and c1 == 0:  # 对方说的数字你一个也没拿
                    self.op_uncover()
                    return
                elif weight == 0 and c1 == 1:  # 我只有一个1, 就欺骗对方, 将总和加1
                    self.op_guess = [4, self.my_guess[1]]
                elif weight == 0 and c1 == 2:  # 有2个1, 继续欺骗
                    self.op_guess = [4, self.my_guess[1]]
                elif weight == 0:  # 自己拿了3个不一样的, 也没有对方说的, 揭了
                    self.op_uncover()
                    return
                elif weight == 1 and c1 == 0:  # 有一个数字相同, 但是没有1
                    if c2 != 0:  # 剩下两个都是一样的, 就
                        for dice in self.op_dice:
                            if dice != self.my_guess[1]:
                                if dice > self.my_guess[1]:
                                    self.op_guess = [3, dice]
                                else:
                                    self.op_guess = [4, self.my_guess[1]]
                                break
                    else:  # 剩下两个不一样,猜其中的一个,或者往高了猜
                        flag = 0
                        for dice in self.op_dice:
                            if dice != self.my_guess[1]:
                                if dice > self.my_guess[1]:
                                    self.op_guess = [3, dice]
                                    flag = 1
                        if flag == 0:
                            self.op_guess = [4, self.my_guess[1]]
                elif weight == 1 and c1 == 1:  # 有一个相同, 且有一个1
                    temp = 0  # 找出那个不同的
                    for dice in self.op_dice:
                        if dice != self.my_guess[1]:
                            temp = dice
                    if temp > self.my_guess[1] and randint(0, 2) >= 1:  # 有2/3的概率选自己的那一个
                        self.op_guess = [3, temp]
                    else:
                        self.op_guess = [4, self.my_guess[1]]
                elif weight == 1 and c1 >= 2:  # 有一个相同, 且有2个1
                    self.op_guess = [4, self.my_guess[1]]
                elif weight == 2 and c1 == 0:  # 有两个相同, 没有1
                    self.op_guess = [4, self.my_guess[1]]
                elif weight == 2 and c1 == 1:  # 有两个相同且有一个1
                    self.op_guess = [4, self.my_guess[1]]
                elif weight == 3:
                    self.op_guess = [5, self.my_guess[1]]
                else:
                    self.op_uncover()
                    return

            if self.my_guess[0] == 4:
                if weight == 0 and c1 == 0:
                    self.op_uncover()
                    return
                elif weight == 0 and c1 == 1:
                    self.op_uncover()
                    return
                elif weight == 0 and c1 >= 2:
                    self.op_guess = [5, self.my_guess[1]]
                elif weight == 1 and c1 == 0:
                    self.op_uncover()
                    return
                elif weight == 1 and c1 == 1:  # 这种情况一般机器人就输了, 因为高不成低不就
                    temp = 0
                    for dice in self.op_dice:
                        if dice != self.my_guess[1] and dice != 1:
                            temp = dice
                            break
                    if temp > self.my_guess[1] and randint(0, 2) == 1:
                        self.op_guess = [4, temp]
                    else:
                        self.op_guess = [5, self.my_guess[1]]
                elif weight == 1 and c1 == 2:
                    self.op_guess = [5, self.my_guess[1]]
                elif weight == 2 and c1 == 0:  # 这种也很不好猜
                    self.op_uncover()
                    return
                elif weight == 2 and c1 == 1:
                    self.op_guess = [5, self.my_guess[1]]
                elif weight == 3:
                    self.op_guess = [5, self.my_guess[1]]
                else:
                    self.op_uncover()
                    return
            if self.my_guess[0] == 5:
                if weight + c1 != 3:
                    self.op_uncover()
                    return
                else:
                    self.op_guess = [6, self.my_guess[1]]
            if self.my_guess[0] == 6:
                self.op_uncover()
                return

        temp = "不知道" if self.op_guess[1] == 0 else str(self.op_guess[1])
        self.guess_view.append("对手 " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\n" +
                               str(self.op_guess[0]) + "个" + temp)

    def op_uncover(self):
        total_list = self.op_dice + self.my_dice
        if total_list.count(self.my_guess[1]) + total_list.count(1) >= self.my_guess[0]:
            self.win_hint.setText("你赢了")
        else:
            self.win_hint.setText("你输了")
        self.op_dice_lb.setText(
            "对方骰子: " + str(self.op_dice[0]) + ',' + str(self.op_dice[1]) + ',' + str(self.op_dice[2]))


app = QApplication(sys.argv)
qb = Brag()
qb.show()
sys.exit(app.exec_())
