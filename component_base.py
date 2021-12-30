"""Base class for all app components"""
import streamlit as st


class Component:
	"""Base component"""
	def __init__(self, container: st.container):
		self.container = container
