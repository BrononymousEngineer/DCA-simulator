"""All relevant plots"""
import component_base
import plotly.graph_objects as go

import numpy as np
import streamlit as st


class LinePlot(component_base.Component):
	"""Basic plotly chart"""
	def __init__(self, container: st.container, time_unit: str):
		super().__init__(container)
		self.figure = go.Figure()
		self.time_unit = time_unit

	def render(self):
		"""Actually show the chart"""
		self.figure.update_layout(
			autosize=False,
			width=600,
			height=775,
			margin=dict(
				l=50,
				r=50,
				b=50,
				t=50,
				pad=4
			),
			xaxis_title='Days',
			yaxis_title='Total Account Balance ($)'
			# paper_bgcolor="LightSteelBlue",
		)
		self.container.plotly_chart(self.figure, use_container_width=True)

	def add_line(self, values: np.array, name: str):
		"""Add a series to the plot"""
		x = np.array(range(len(values)))
		self.figure.add_trace(
			go.Scatter(x=x, y=values, name=name)
		)