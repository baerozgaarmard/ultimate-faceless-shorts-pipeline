#!/usr/bin/env python3
"""
Quick shortcut to launch the Interactive Video Style Chooser with Reference Images.
"""
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
installer = os.path.join(script_dir, "install.py")
os.system(f'"{sys.executable}" "{installer}" --choose-style')
