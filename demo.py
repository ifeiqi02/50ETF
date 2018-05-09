#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Author:Qingshui Wang
# @Email:apecoder@foxmail.com
# @Time:2018/4/29 8:54
# @File:demo.py
"""
import sys
import random

from PyQt5.QtWidgets import QPushButton, QMainWindow, QSizePolicy, QWidget, QListWidget, QMessageBox, QTableView, \
    QListView, QHeaderView, \
    QVBoxLayout, QApplication, QTreeView, QAbstractItemView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QStringListModel, QTimer

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np


class Table(QWidget):
    def __init__(self, arg=None):
        super(Table, self).__init__(arg)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("QTableView例子")
        self.resize(500, 300)
        self.model = QStandardItemModel(4, 4)
        self.model.setHorizontalHeaderLabels(['title1', 'title2', 'title3', 'title4'])

        for row in range(4):
            for col in range(4):
                item = QStandardItem("row %s, column %s" % (row, col))
                self.model.setItem(row, col, item)

        self.tableView = QTableView()
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        dlglayout = QVBoxLayout()
        dlglayout.addWidget(self.tableView)
        self.setLayout(dlglayout)


class ListViewDemo(QWidget):
    def __init__(self, parent=None):
        super(ListViewDemo, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("QListView Demo")
        self.resize(300, 270)
        layout = QVBoxLayout()

        listView = QListView()
        slm = QStringListModel()
        self.qList = ['item1', 'item2', 'item3', 'item4']
        slm.setStringList(self.qList)
        listView.setModel(slm)
        listView.clicked.connect(self.clicked)
        layout.addWidget(listView)
        self.setLayout(layout)

    def clicked(self, qModelIndex):
        QMessageBox.information(self, "ListWidget", "You choose " + self.qList[qModelIndex.row()])


class ListWidget(QListWidget):
    def __init__(self, parent=None):
        super(ListWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.resize(300, 120)
        self.addItem("item1")
        self.addItem("item2")
        self.addItem("item3")
        self.addItem("item4")
        self.setWindowTitle("QListWidget 例子")
        self.itemClicked.connect(self.clicked)

    def clicked(self, QModelIndex):
        QMessageBox.information(self, "hahhah", "You choose :" + QModelIndex.text())


class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        # super(MyMplCanvas, self).__init__(parent)
        plt.rcParams['font.family'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        self.axes.hold(False)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        # FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        # FigureCanvas.updateGeometry(self)

    def start_static_plot(self):
        self.fig.suptitle("测试静态图")
        t = np.arange(0.0, 3.0, 0.01)
        s = np.sin(2 * np.pi * t)
        self.axes.plot(t, s)
        self.axes.set_xlabel("静态图：X轴")
        self.axes.set_ylabel("静态图：Y轴")
        self.axes.grid(True)

    def start_dynamic_plot(self):
        timer = QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)

    def update_figure(self):
        self.fig.suptitle("测试动态图")
        l = [np.random.randint(0, 10) for i in range(4)]
        self.axes.plot([0, 1, 2, 3], l, 'r')
        self.axes.set_xlabel("动态图：X轴")
        self.axes.set_ylabel("动态图：Y轴")
        self.axes.grid(True)
        self.draw()


class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.mpl = MyMplCanvas(self, width=5, height=4, dpi=100)
        self.mpl_ntb = NavigationToolbar(self.mpl, self)
        self.layout.addWidget(self.mpl)
        self.layout.addWidget(self.mpl_ntb)


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.left = 10
        self.top = 10
        self.title = 'PyQt5 matplotlib example - pythonspot.com'
        self.width = 640
        self.height = 400
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        m = PlotCanvas(self, width=5, height=4)
        m.move(0, 0)

        button = QPushButton('PyQt5 button', self)
        button.setToolTip('This s an example button')
        button.move(500, 0)
        button.resize(140, 100)

        self.show()


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()

    def plot(self):
        data = [random.random() for i in range(25)]
        ax = self.figure.add_subplot(111)
        ax.plot(data, 'r-')
        ax.set_title('PyQt Matplotlib Example')
        self.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = App()
    win.show()
    sys.exit(app.exec_())
