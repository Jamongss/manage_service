#!/usr/bin/python
# -*- coding:utf-8 -*-

"""program"""
__author__ = "Maum.Ai - Jamong"
__date__ = "creation: 2024-10-13, modification: 2024-10-29"

###########
# imports #
###########
import time
from datetime import datetime

#########
# class #
#########
class ElapsedTime:
    def __init__(self):
        self.proc_start_time = datetime.fromtimestamp(time.time())

    def run(self):
        end_time = datetime.fromtimestamp(time.time())
        required_time = end_time - self.proc_start_time

        return self.proc_start_time, required_time
