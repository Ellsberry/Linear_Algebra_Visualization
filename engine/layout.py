"""Shared layout helpers — consistent two-column skeleton for every topic."""
import streamlit as st


def two_col(ratio=0.4):
    """Return (left, right) columns at the given width ratio."""
    return st.columns([ratio, 1 - ratio], gap="large")
