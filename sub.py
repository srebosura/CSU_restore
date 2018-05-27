#!/usr/bin/env python
import subprocess
import os,sys

stdouterr = os.popen4('python exec_cmd.py "csu_pwrctrl -g vbat1" 20 |tail -2 |head -1')[1].read()
print(stdouterr)
