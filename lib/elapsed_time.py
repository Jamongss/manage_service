#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""program"""
__author__ = "Jamongss"
__date__ = "2024-10-13"
__last_modified_by__ = "Jamongss"
__last_modified_date__ = "2025-10-01"
__maintainer__ = "Jamongss"

###########
# imports #
###########
import time
import traceback
from datetime import datetime

#########
# class #
#########
class ElapsedTime:
    def __init__(self):
        self.proc_start_time = datetime.fromtimestamp(time.time())

    def run(self):
        try:
            end_time = datetime.fromtimestamp(time.time())
            required_time = end_time - self.proc_start_time

            return self.proc_start_time, required_time
        except Exception:
            raise Exception(traceback.format_exc())

