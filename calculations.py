"""All relevant calculations

References
----------
simple to log returns
	https://quant.stackexchange.com/questions/47537/convert-arithmetic-returns-to-log-returns
"""
import streamlit as st
import math
import numpy as np


def calc_returns(
	total_days: int,
	total_cash: float,
	invest_amt: float,
	invest_frq: float,
	simple_annual_ret: float,
	simple_annual_vol: float,
	simple_annual_div: float,
	div_freq: float
):
	"""Calculate return series"""
	year_days = 365
	# Convert simple returns to log returns
	log_annual_ret = math.log(1 + simple_annual_ret, math.e)
	log_annual_vol = math.log(1 + simple_annual_vol, math.e)
	log_annual_div = math.log(1 + simple_annual_div, math.e)
	# Convert to daily log returns
	log_daily_ret = log_annual_ret / year_days
	log_daily_vol = log_annual_vol / math.sqrt(year_days)
	# Convert to incremental div
	log_inc_div = log_annual_div*(div_freq / year_days)
	# Calculate return series
	returns = np.array([
		(log_daily_ret - (0.5*(log_daily_vol**2))) + log_daily_vol*w
		for w in np.random.normal(loc=0, scale=1, size=total_days)
	])
	returns[[
		x for x in range(1, total_days + 1) if x % div_freq == 0
	]] += log_inc_div
	returns = np.array([0] + list(returns))
	# Calculate cash amounts
	lump_sum_current = total_cash
	lump_sum_cash = np.zeros(len(returns))
	dca_current = 0
	dca_cash = np.zeros(len(returns))
	dca_total = dca_current
	for idx, ret in np.ndenumerate(returns):
		i = idx[0]
		lump_sum_current = lump_sum_current*math.exp(ret)
		lump_sum_cash[i] = lump_sum_current
		dca_current = dca_current*math.exp(ret)
		if i % invest_frq == 0:
			dca_current += invest_amt
			dca_total += invest_amt
		dca_cash[i] = dca_current
	return lump_sum_cash, dca_cash
