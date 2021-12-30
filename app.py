"""Main app

Disclaimer
----------
This was made quickly so there is some pointless code here and there.
I probably don't need to use the session_state at all.
"""
import calculations
import controls
import plots
import streamlit as st

st.set_page_config(
	page_title='DCA Simulator',
	page_icon='💲',
	layout='wide'
)


def add_to_state(name: str, obj: object):
	"""Function for adding things to state. Seems unnecessary but should help
	with traceability."""
	setattr(st.session_state, name, obj)


def setup_time_controls(sidebar: st.sidebar):
	"""Controls related to investment duration and frequency"""
	investment_controls = sidebar.expander(
		label='DCA Strategy', expanded=False
	)
	investment_amount = controls.FloatBox(
		container=investment_controls,
		label='Invest:',
		help_txt='''
		This is how much is to be periodically invested.
		''',
		min_val=1.0, max_val=1000000.0, increment=0.01, default_val=500.0,
		precision=2
	); add_to_state('investment_freq_amount', investment_amount.raw)
	investment_frequency = controls.TimeRange(
		container=investment_controls,
		label='every:',
		help_txt='''
		This is how often money is invested.
		''',
		min_val=1, max_val=365, increment=1, default_val=1, default_idx=2
	); add_to_state('investment_freq_days', investment_frequency.total_days)
	investment_period = controls.TimeRange(
		container=investment_controls,
		label='over a period of:',
		help_txt='''
		This is the total time period over which investing takes place.
		''',
		min_val=1, max_val=365, increment=1, default_val=1, default_idx=3
	); add_to_state('total_days', investment_period.total_days)
	add_to_state('time_unit', investment_period.unit)
	total_cash = sum([
		st.session_state.investment_freq_amount
		for i in range(st.session_state.total_days + 1)
		if i % st.session_state.investment_freq_days == 0
	])
	add_to_state('total_cash', total_cash)
	investment_controls.markdown(
		'''A total of **${:.2f}** is invested.'''.format(
			total_cash
	))


def setup_investment_controls(sidebar: st.sidebar):
	"""Controls related to investment behavior"""
	behavior_controls = sidebar.expander(
		label='Asset Behavior', expanded=False
	)
	behavior_controls.markdown('''
	###### Asset behavior is modeled with [Geometric Brownian Motion](https://en.wikipedia.org/wiki/Geometric_Brownian_motion#:~:text=Geometric%20Brownian%20motion%20is%20used,model%20of%20stock%20price%20behavior.&text=A%20GBM%20process%20only%20assumes,see%20in%20real%20stock%20prices.)
	''')
	annualized_return = controls.FloatBox(
		container=behavior_controls,
		label='Annualized Return',
		help_txt='''
		This is the average yearly return over the selected time period. 
		The number in the box below is really a percentage, so 0.085 = 8.5%
		''',
		min_val=0.0, max_val=10000.0, increment=0.001, default_val=0.085,
	); add_to_state('annualized_return', annualized_return.raw)
	annualized_volatility = controls.FloatBox(
		container=behavior_controls,
		label='Annualized Volatility',
		help_txt='''
		This is the average yearly volatility over the selected time period. 
		The number in the box below is really a percentage, so 0.2 = 2%
		''',
		min_val=0.0, max_val=10000.0, increment=0.001, default_val=0.0,
	); add_to_state('annualized_volatility', annualized_volatility.raw)
	annualized_div_yield = controls.FloatBox(
		container=behavior_controls,
		label='Annualized Dividend Yield',
		help_txt='''
		This is the average yearly dividend yield over the selected time period. 
		The number in the box below is really a percentage, so 0.035 = 3.5%
		''',
		min_val=0.0, max_val=1.0, increment=0.001, default_val=0.0,
	); add_to_state('annualized_div_yield', annualized_div_yield.raw)
	div_payment_frequency = controls.TimeRange(
		container=behavior_controls,
		label='Dividend paid every:',
		help_txt='''
		This is how often a dividend is paid.
		''',
		min_val=1, max_val=365, increment=1, default_val=3, default_idx=2
	); add_to_state('div_freq_days', div_payment_frequency.total_days)


def setup_sidebar():
	"""Setup controls in the sidebar"""
	sidebar = st.sidebar
	# if sidebar.checkbox('Show app state'):
	# 	st.write(st.session_state)
	info_container = sidebar.expander('App Info', expanded=True)
	info_container.info('''
	**Summary** - The chart shows the total account balance of two strategies 
	for investing in an asset (that behaves according to the **Asset Behavior** 
	controls below). 
	''')
	info_container.warning('''
	*Strategy 1* - Invest all money in one lump sum at the beginning of the period 
	''')
	info_container.warning('''
	*Strategy 2* - Dollar cost average into the investment according to the 
	parameters that are set in the **DCA Strategy** below 
	''')
	setup_time_controls(sidebar)
	setup_investment_controls(sidebar)
	if sidebar.checkbox('To do:'):
		sidebar.markdown('''
		- fix DCA strategy bug that causes an array index error (happens rarely) 
		- format the graph in a better way (better hoverbox comparison)
		- add option to change the graph between total account balance and 
		total return
		- have a help page that better explains what the controls do
		- clean up the code
		- other stuff I forget at the moment
		''')


def main():
	"""Run app"""
	setup_sidebar()
	lump_sum_cash, dca_cash = calculations.calc_returns(
		total_days=st.session_state.total_days,
		total_cash=st.session_state.total_cash,
		invest_amt=st.session_state.investment_freq_amount,
		invest_frq=st.session_state.investment_freq_days,
		simple_annual_ret=st.session_state.annualized_return,
		simple_annual_vol=st.session_state.annualized_volatility,
		simple_annual_div=st.session_state.annualized_div_yield,
		div_freq=st.session_state.div_freq_days
	)
	plot = plots.LinePlot(st, st.session_state.time_unit)
	plot.add_line(lump_sum_cash, name='Lump Sum')
	plot.add_line(dca_cash, name='DCA')
	plot.render()


if __name__ == '__main__':
	main()
