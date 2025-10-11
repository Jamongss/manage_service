#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""program"""
__author__ = "Jamongss"
__date__ = "2023-01-25"
__last_modified_by__ = "Jamongss"
__last_modified_date__ = "2025-10-01"
__maintainer__ = "Jamongss"

###########
# imports #
###########
import os
import sys
import traceback
from cfg.config import RestartConfig
from lib.logger import get_timed_rotating_logger
from lib.control_svctl import Svctl
from lib.elapsed_time import ElapsedTime

###################
# global variable #
###################
manage_root = os.path.dirname(os.path.abspath(__file__))

#########
# class #
#########
class RestartService:
    def __init__(self):
        # Set logger
        self.log = get_timed_rotating_logger(
            logger_name=RestartConfig.logger_name,
            log_dir_path=os.path.join(manage_root, RestartConfig.log_dir_path),
            log_file_name=RestartConfig.log_file_name,
            backup_count=RestartConfig.backup_count,
            log_level=RestartConfig.log_level
        )

    def run(self):
        """
        This is a program that restart service
        """
        # Set time
        elapsed_time = ElapsedTime()

        self.log.info("-" * 100)
        self.log.info("[START] Restart service")
        self.log.info("-" * 100)

        program_list = RestartConfig.service_list
        # program_list = ['col_rest_api']

        try:
            c_svctl = Svctl(self.log, program_list)
            c_svctl.control(action='stop')
            c_svctl.control(action='start')
        except Exception:
            exc_info = traceback.format_exc()
            self.log.error(exc_info)
        finally:
            proc_start_time, required_time = elapsed_time.run()
            self.log.info(
                "[E N D] Start time = {}, The time required = {}".format(
                    proc_start_time, required_time)
            )


########
# main #
########
if __name__ == '__main__':
    restart_service = RestartService()
    restart_service.run()

