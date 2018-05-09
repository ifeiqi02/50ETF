#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Author:Qingshui Wang
# @Email:apecoder@foxmail.com
# @Time:2018/4/9 17:19
# @File:Option.py
"""
import copy
from datetime import datetime

import numpy as np
import pandas as pd
from scipy.stats import norm


# class Option(object):
#     """
#     Args:
#         spot: spot price
#         strike: strike price
#         riskfree: riskfree rate
#         dividend: dividend rate
#         duration: time to expire
#         vol: volatility of underlying asset
#         n_steps: number of time steps
#         n_paths: number of paths
#         dt: delta t
#         paths: the sample paths'
#         omega: 1 for call, -1 for put
#     """
#
#     def __init__(self, S, K, rf, q, T, vol, n_steps, n_paths, omega=1):
#         self.spot = S
#         self.strike = K
#         self.riskfree = rf
#         self.dividend = q
#         self.duration = T
#         self.vol = vol
#         self.n_steps = n_steps
#         self.n_paths = n_paths
#         self.dt = self.duration / self.n_steps
#         self.omega = omega
#         self.paths = self.MC_simulate()
#
#     def MC_simulate(self):
#         paths = np.zeros((self.n_steps + 1, self.n_paths))
#         rands = np.random.standard_normal((self.n_steps, self.n_paths))
#         paths[1:, :] = self.spot * np.cumprod(np.exp((self.riskfree - self.dividend - self.vol ** 2 / 2) * self.dt
#                                                      - self.vol * np.sqrt(self.dt) * rands), axis=0)
#         paths[0] = self.spot
#         return paths
#
#     def MC_pricing(self):
#         return np.exp(-self.riskfree * self.duration) * np.sum(
#             np.maximum(self.omega * (self.paths[-1] - self.strike), 0)) / self.n_paths
#
#     def BS_pricing(self):
#         d1 = (np.log(self.spot / self.strike) + (self.riskfree - self.dividend + self.vol ** 2 / 2) * self.duration) \
#              / (self.vol * np.sqrt(self.duration))
#         d2 = d1 - self.vol * np.sqrt(self.duration)
#         return self.omega * self.spot * np.exp(-self.dividend * self.duration) * norm.cdf(self.omega * d1) \
#                - self.omega * self.strike * np.exp(-self.riskfree * self.duration) * norm.cdf(self.omega * d2)


class BasicOption(object):
    def __init__(self):
        self._underlying_close_price = None
        self._dividend = 0.0
        self._expiry_date = None
        self._trade_date = None