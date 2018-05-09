#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Author:Qingshui Wang
# @Email:apecoder@foxmail.com
# @Time:2018/4/28 23:13
# @File:UIManage.py
"""
import sys

from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QGridLayout, QVBoxLayout, QHBoxLayout, QTreeWidget, \
    QTreeWidgetItem, QSizePolicy
from PyQt5.QtGui import QIcon
import numpy as np
import matplotlib

matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.ticker as ticker
import matplotlib.dates as mdate

from DataManage import DataManage


class MyMplCanvas(FigureCanvas):
    """
    通过继承FigureCanvas类，使得该类既是一个PyQt5的Qwidget，
    又是一个matplotlib的FigureCanvas，这是连接pyqt5与matplotlib的关键
    """

    def __init__(self, parent=None):
        plt.rcParams['font.family'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

        # 创建一个Figure，
        # 注意：该Figure为matplotlib下的figure，不是matplotlib.pyplot下面的figure
        self.figure = Figure(figsize=(0.8,0.8),facecolor='#171717')

        # 调用figure下面的add_subplot方法，类似于matplotlib.pyplot下面的subplot方法
        self.axes_right = self.figure.add_subplot(211, facecolor='#171717')
        self.axes_right.grid(True, color='red', ls=":")
        self.axes_right.spines['bottom'].set_color("w")
        self.axes_right.spines['top'].set_color("w")
        self.axes_right.spines['left'].set_color("w")
        self.axes_right.spines['right'].set_color("w")
        self.axes_right.tick_params(axis='y', colors='w')
        self.axes_right.tick_params(axis='x', colors='w')
        self.axes_left = self.axes_right.twinx()
        self.axes_left.tick_params(axis='y', colors='w')

        self.axes_bottem = self.figure.add_subplot(212, facecolor='#171717')
        self.axes_bottem.grid(True, color='red', ls=":")
        self.axes_bottem.spines['bottom'].set_color("w")
        self.axes_bottem.spines['top'].set_color("w")
        self.axes_bottem.spines['left'].set_color("w")
        self.axes_bottem.spines['right'].set_color("w")
        self.axes_bottem.tick_params(axis='y', colors='w')
        self.axes_bottem.tick_params(axis='x', colors='w')

        # 初始化父类
        FigureCanvas.__init__(self, self.figure)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)

    # def


class MainWindow(object):
    def __init__(self):
        self.setWindowTitle("50ETF期权监控系统")
        self.resize(1000, 600)
        self.setWindowIcon(QIcon("50ETF.ico"))

        self.code_lbl = QLabel("代码")
        self.name_lbl = QLabel("名称")
        self.last_lbl = QLabel("现价")
        self.chg_lbl = QLabel("涨跌")
        self.pct_chg_lbl = QLabel("涨跌幅")
        self.open_lbl = QLabel("今开")
        self.high_lbl = QLabel("最高")
        self.low_lbl = QLabel("最低")
        self.vol_lbl = QLabel("成交量")
        self.amt_lbl = QLabel("成交额")
        self.time_lbl = QLabel("时间")

        self.code_data_lbl = QLabel("510050")
        self.name_data_lbl = QLabel("50ETF")
        self.last_data_lbl = QLabel()
        self.chg_data_lbl = QLabel()
        self.pct_chg_data_lbl = QLabel()
        self.open_data_lbl = QLabel()
        self.high_data_lbl = QLabel()
        self.low_data_lbl = QLabel()
        self.vol_data_lbl = QLabel()
        self.amt_data_lbl = QLabel()
        self.time_data_lbl = QLabel()

        etf_layout = QGridLayout()
        etf_layout.setSpacing(10)
        etf_layout.addWidget(self.code_lbl, 0, 0)
        etf_layout.addWidget(self.code_data_lbl, 1, 0)
        etf_layout.addWidget(self.name_lbl, 0, 1)
        etf_layout.addWidget(self.name_data_lbl, 1, 1)
        etf_layout.addWidget(self.last_lbl, 0, 2)
        etf_layout.addWidget(self.last_data_lbl, 1, 2)
        etf_layout.addWidget(self.chg_lbl, 0, 3)
        etf_layout.addWidget(self.chg_data_lbl, 1, 3)
        etf_layout.addWidget(self.pct_chg_lbl, 0, 4)
        etf_layout.addWidget(self.pct_chg_data_lbl, 1, 4)
        etf_layout.addWidget(self.open_lbl, 0, 5)
        etf_layout.addWidget(self.open_data_lbl, 1, 5)
        etf_layout.addWidget(self.high_lbl, 0, 6)
        etf_layout.addWidget(self.high_data_lbl, 1, 6)
        etf_layout.addWidget(self.low_lbl, 0, 7)
        etf_layout.addWidget(self.low_data_lbl, 1, 7)
        etf_layout.addWidget(self.vol_lbl, 0, 8)
        etf_layout.addWidget(self.vol_data_lbl, 1, 8)
        etf_layout.addWidget(self.amt_lbl, 0, 9)
        etf_layout.addWidget(self.amt_data_lbl, 1, 9)
        etf_layout.addWidget(self.time_lbl, 0, 10)
        etf_layout.addWidget(self.time_data_lbl, 1, 10)

        self.call_lbl = QLabel("认购/看涨")
        self.put_lbl = QLabel("认沽/看跌")

        option_type_layout = QHBoxLayout()
        option_type_layout.addWidget(self.call_lbl)
        option_type_layout.addWidget(self.put_lbl)

        self.option_data_tree = QTreeWidget()
        self.option_data_tree.setColumnCount(13)
        self.option_data_tree.setHeaderLabels(["最新价", "涨跌幅", "成交量", "持仓量", "隐含波动率", "Delta",
                                               "行权价",
                                               "Delta", "隐含波动率", "持仓量", "成交量", "涨跌幅", "最新价"])
        self.cur_month = QTreeWidgetItem(self.option_data_tree)
        self.cur_month.setText(0, "当月合约")
        self.cur_month_strike1 = QTreeWidgetItem(self.cur_month)
        self.cur_month_strike2 = QTreeWidgetItem(self.cur_month)
        self.cur_month_strike3 = QTreeWidgetItem(self.cur_month)
        self.cur_month_strike4 = QTreeWidgetItem(self.cur_month)
        self.cur_month_strike5 = QTreeWidgetItem(self.cur_month)
        self.cur_month_strike6 = QTreeWidgetItem(self.cur_month)
        self.cur_month_strike7 = QTreeWidgetItem(self.cur_month)
        self.cur_month_strike8 = QTreeWidgetItem(self.cur_month)
        self.cur_month_strike9 = QTreeWidgetItem(self.cur_month)
        self.cur_month_strike10 = QTreeWidgetItem(self.cur_month)
        self.cur_month_strike11 = QTreeWidgetItem(self.cur_month)
        self.next_month = QTreeWidgetItem(self.option_data_tree)
        self.next_month.setText(0, "下月合约")
        self.next_month_strike1 = QTreeWidgetItem(self.next_month)
        self.next_month_strike2 = QTreeWidgetItem(self.next_month)
        self.next_month_strike3 = QTreeWidgetItem(self.next_month)
        self.next_month_strike4 = QTreeWidgetItem(self.next_month)
        self.next_month_strike5 = QTreeWidgetItem(self.next_month)
        self.next_month_strike6 = QTreeWidgetItem(self.next_month)
        self.next_month_strike7 = QTreeWidgetItem(self.next_month)
        self.next_month_strike8 = QTreeWidgetItem(self.next_month)
        self.next_month_strike9 = QTreeWidgetItem(self.next_month)
        self.next_month_strike10 = QTreeWidgetItem(self.next_month)
        self.next_month_strike11 = QTreeWidgetItem(self.next_month)
        self.follew_quar_month1 = QTreeWidgetItem(self.option_data_tree)
        self.follew_quar_month1.setText(0, "随后季月1")
        self.follew_quar_month1_strike1 = QTreeWidgetItem(self.follew_quar_month1)
        self.follew_quar_month1_strike2 = QTreeWidgetItem(self.follew_quar_month1)
        self.follew_quar_month1_strike3 = QTreeWidgetItem(self.follew_quar_month1)
        self.follew_quar_month1_strike4 = QTreeWidgetItem(self.follew_quar_month1)
        self.follew_quar_month1_strike5 = QTreeWidgetItem(self.follew_quar_month1)
        self.follew_quar_month1_strike6 = QTreeWidgetItem(self.follew_quar_month1)
        self.follew_quar_month1_strike7 = QTreeWidgetItem(self.follew_quar_month1)
        self.follew_quar_month1_strike8 = QTreeWidgetItem(self.follew_quar_month1)
        self.follew_quar_month1_strike9 = QTreeWidgetItem(self.follew_quar_month1)
        self.follew_quar_month1_strike10 = QTreeWidgetItem(self.follew_quar_month1)
        self.follew_quar_month1_strike11 = QTreeWidgetItem(self.follew_quar_month1)
        self.follew_quar_month2 = QTreeWidgetItem(self.option_data_tree)
        self.follew_quar_month2.setText(0, "随后季月2")
        self.follew_quar_month2_strike1 = QTreeWidgetItem(self.follew_quar_month2)
        self.follew_quar_month2_strike2 = QTreeWidgetItem(self.follew_quar_month2)
        self.follew_quar_month2_strike3 = QTreeWidgetItem(self.follew_quar_month2)
        self.follew_quar_month2_strike4 = QTreeWidgetItem(self.follew_quar_month2)
        self.follew_quar_month2_strike5 = QTreeWidgetItem(self.follew_quar_month2)
        self.follew_quar_month2_strike6 = QTreeWidgetItem(self.follew_quar_month2)
        self.follew_quar_month2_strike7 = QTreeWidgetItem(self.follew_quar_month2)
        self.follew_quar_month2_strike8 = QTreeWidgetItem(self.follew_quar_month2)
        self.follew_quar_month2_strike9 = QTreeWidgetItem(self.follew_quar_month2)
        self.follew_quar_month2_strike10 = QTreeWidgetItem(self.follew_quar_month2)
        self.follew_quar_month2_strike11 = QTreeWidgetItem(self.follew_quar_month2)
        self.option_data_tree.expandAll()

        option_data_layout = QVBoxLayout()
        option_data_layout.addWidget(self.option_data_tree)

        option_layout = QVBoxLayout()
        option_layout.addLayout(option_type_layout)
        option_layout.addLayout(option_data_layout)

        self.etf_mpl = MyMplCanvas()
        self.option_mpl = MyMplCanvas()
        self.iv_mpl = MyMplCanvas()

        plot_layout = QHBoxLayout()
        plot_layout.addWidget(self.etf_mpl)
        plot_layout.addWidget(self.option_mpl)
        plot_layout.addWidget(self.iv_mpl)

        main_layout = QGridLayout()
        main_layout.addLayout(etf_layout, 0,0)
        main_layout.addLayout(option_layout, 1,0)
        main_layout.addLayout(plot_layout, 2,0)
        self.setLayout(main_layout)
        self.showMaximized()


class MWController(QWidget, MainWindow):
    def __init__(self):
        super(MWController, self).__init__()
        self.data_manage = DataManage()
        self.update_50etf()
        self.update_option_data()
        self.update_etf_plot()

    def update_50etf(self):
        data = self.data_manage.get_cur_50ETF()
        self.last_data_lbl.setText(data['RT_LAST'][0])
        self.chg_data_lbl.setText(data['RT_CHG'][0])
        self.pct_chg_data_lbl.setText(data['RT_PCT_CHG'][0])
        self.open_data_lbl.setText(data['RT_OPEN'][0])
        self.high_data_lbl.setText(data['RT_HIGH'][0])
        self.low_data_lbl.setText(data['RT_LOW'][0])
        self.vol_data_lbl.setText(data['RT_VOL'][0])
        self.amt_data_lbl.setText(data['RT_AMT'][0])
        self.time_data_lbl.setText(data['RT_TIME'][0])

    def update_option_data(self):
        # cur_contracts_df = self.data_manage.get_cur_contracts()

        self.cur_month_strike1.setText(0, "hello")
        self.cur_month_strike1.setText(1, "world")

    def update_etf_plot(self):
        def format_date(x, pos=None):
            thisind = np.clip(int(x + 0.5), 0, len(last_etf_data) - 1)
            return last_etf_data.index.time[thisind].strftime('%H-%M')

        last_etf_data = self.data_manage.get_last_50ETF_by_minute()
        last_list = last_etf_data['close']
        per_chg_list = [(last_list[i] - last_list[0]) / last_list[0] for i in range(len(last_list))]
        xtick_list = np.arange(len(last_etf_data))
        self.etf_mpl.axes_right.plot(xtick_list, last_etf_data['close'],"w",linewidth=1)
        self.etf_mpl.axes_left.plot(xtick_list, last_etf_data['macd_diff'], 'gold',linewidth=1)
        self.etf_mpl.axes_bottem.bar(xtick_list,last_etf_data['volume'],color="gold")
        self.etf_mpl.axes_bottem.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
        self.etf_mpl.figure.autofmt_xdate()
        self.etf_mpl.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MWController()
    win.show()
    sys.exit(app.exec_())
