"""
Lecture 14.1: Mini-Project Overview — Choosing Your Question and Network Design

In order to get rid of Brian2 warnings, you can use g++ compiler when launching the script:
> CC=gcc CXX=g++ python lecture_13_XXX.py
"""
# flake8: noqa: F403,F405
# mypy: disable-error-code=name-defined

import warnings

import brian2
import matplotlib.pyplot as plt

# Standard project setup — Week 14 mini-project
import numpy as np
from brian2 import *
from scipy import signal

warnings.filterwarnings("ignore")

# Always call start_scope() at the beginning of each simulation block
start_scope()
seed(42)  # Reproducibility

# Standard LIF parameters — use these unless your project specifically varies them
tau = 20 * ms
v_rest = -65 * mV
v_thresh = -50 * mV
v_reset = -65 * mV
R = 10 * Mohm

print("Week 14 Mini-Project environment ready.")
print("Brian2 version:", brian2.__version__)
