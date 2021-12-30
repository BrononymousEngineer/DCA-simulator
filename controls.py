"""User controls"""
import component_base
import streamlit as st
from typing import Union


class FloatBox(component_base.Component):
	"""User control to set annualized return"""
	def __init__(
			self,
			container: st.container,
			label: str,
			help_txt: str,
			min_val: float,
			max_val: float,
			increment: float,
			default_val: float,
			precision: int = 3
	):
		super().__init__(container)
		self.__annualized_return = self.container.number_input(
			label=label,
			min_value=min_val,
			max_value=max_val,
			value=default_val,
			step=increment,
			format='%.{}f'.format(precision),
			help=help_txt
		)

	@property
	def raw(self) -> float:
		"""Raw value"""
		return float('{:.3f}'.format(self.__annualized_return))

	@property
	def fmt(self) -> str:
		"""Formatted value"""
		value = round(self.raw * 100, 1)
		decimal = int(str(value).split('.')[1])
		return f'{int(value) if decimal == 0 else value}%'


class TimeRange(component_base.Component):
	"""Set the overall investment period"""
	def __init__(
			self,
			container: st.container,
			label: str,
			help_txt: str,
			min_val: Union[int, float],
			max_val: Union[int, float],
			increment: Union[int, float],
			default_val: Union[int, float],
			default_idx: int
	):
		super().__init__(container)
		cols = self.container.columns([3, 2])
		value = cols[0].number_input(
			label=label,
			min_value=min_val,
			max_value=max_val,
			step=increment,
			value=default_val
		)
		self.unit = cols[1].selectbox(
			label='',
			options=['days', 'weeks', 'months', 'years'],
			index=default_idx,
			help=help_txt
		)
		self.total_days = int({
			'days': 1,
			'weeks': 7,
			'months': 365 / 12,
			'years': 365
		}[self.unit]*value)
