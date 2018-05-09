#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Author:Qingshui Wang
# @Email:apecoder@foxmail.com
# @Time:2018/4/28 23:23
# @File:DataManage.py
"""
from datetime import datetime
from WindPy import *
import pandas as pd


class DataManage:
    def __init__(self):
        w.start(waitTime=60)

    def get_last_trading_day(self):
        """
        获取离当前最近的交易日。若当前为交易日，返回当前日期，若不是，返回之前最近的一个交易日
        """
        return w.tdaysoffset(0, str(datetime.now().date()), "").Data[0][0]

    @staticmethod
    def get_cur_contracts():
        """
        获取当前流通的50ETF期权合约
        Return:包含当前流通的50ETF期权合约信息的dataframe
        """
        raw = w.wset("optioncontractbasicinfo", "exchange=sse;windcode=510050.SH;status=trading")
        cur_contracts_df = pd.DataFrame(raw.Data).T
        cur_contracts_df.columns = raw.Fields
        cur_contracts_grouped = cur_contracts_df.groupby("limit_month")
        # cur_contracts_df.to_csv("D://tmp.csv",encoding="utf_8_sig")
        for month in map(str, cur_contracts_grouped.groups.keys()):
            cur_contracts_grouped.get_group(month).to_csv("D://" + month + ".csv", encoding="utf_8_sig")

    @staticmethod
    def get_cur_50ETF():
        """
        获取当前50ETF的实时信息
        Return:包含当前50ETF的实时信息的dataframe
        """
        raw = w.wsq("510050.SH", "rt_last,rt_chg,rt_pct_chg,rt_open,rt_high,rt_low,rt_vol,rt_amt,rt_time")
        cur_50ETF_df = pd.DataFrame(raw.Data).T
        cur_50ETF_df.columns = raw.Fields
        return cur_50ETF_df.astype("str")

    def get_last_50ETF_by_minute(self):
        """
        获取最近的50ETF日内跳价数据
        Return: 包含最新价和成交量的Dataframe
        """
        start_time = datetime.combine(self.get_last_trading_day().date(), time(9, 30, 0))
        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # result = w.wst("510050.SH", "last,volume", start_time, end_time, "")
        result = w.wsi("510050.SH", "close,pct_chg,volume,MACD", start_time, end_time, "MACD_L=26;MACD_S=12;MACD_N=9;MACD_IO=1")
        return pd.DataFrame(columns=result.Times,index=result.Fields,data=result.Data).T


if __name__ == '__main__':
    data = DataManage()
    # print(data.get_cur_contracts())
    data.get_last_50ETF_by_minute()
    # print(data.get_last_trading_day())
