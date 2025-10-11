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
import os
import sys
import time
import traceback
import subprocess
sys.path.append('../')
from cfg.config import SUBPROCESSConfig
from logger import get_timed_rotating_logger

###################
# global variable #
###################
manage_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#########
# class #
#########
class TimeoutExpired(Exception):
    def __init__(self, cmd, timeout):
        self.cmd = cmd
        self.timeout = timeout
        super(TimeoutExpired, self).__init__(
            "Command '{}' timed out after {} seconds.".format(cmd, timeout)
        )

class SubProcess:
    def __init__(self, cmd, timeout = 30, **kwargs):
        self.cmd = cmd
        self.timeout = timeout
        self.log = kwargs.get('log', self._setting_logger())
        # self.log.info(f'[SubProcess] Command : {self.cmd}')
        # self.log.info(f'[SubProcess] Timeout : {self.timeout}')

    @staticmethod
    def _setting_logger():
        log = get_timed_rotating_logger(
            logger_name=SUBPROCESSConfig.logger_name,
            log_dir_path=os.path.join(
                manage_root,
                SUBPROCESSConfig.log_dir_path
            ),
            log_file_name=SUBPROCESSConfig.log_file_name,
            backup_count=SUBPROCESSConfig.backup_count,
            log_level=SUBPROCESSConfig.log_level
        )
        return log

    def sub_process_run(self):
        try:
            # subprocess.run을 사용하여 process 시작 및 timeout 설정
            result = subprocess.run(
                self.cmd, shell=True, text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=self.timeout
            )
            # 결과 반환 (stdout, stderr)
            # self.log.info(f'[SubProcess] stdout : {result.stdout}')
            # self.log.info(f'[SubProcess] stderr : {result.stderr}')
            return result.stdout, result.stderr
        except subprocess.TimeoutExpired as e:
            self.log.error(
                "Command '{}' timed out after {} seconds".format(
                    self.cmd, e.timeout
                )
            )
            self.log.error(traceback.format_exc())
            return None, None

    def sub_process_popen(self):
        try:
            # subprocess.Popen을 사용하여 process 시작
            sub_pro = subprocess.Popen(
                self.cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            s_time = time.time()

            # timeout 체크
            while sub_pro.poll() is None:
                if time.time() - s_time >= self.timeout:
                    # timeout 발생 시 process 종료
                    sub_pro.kill()
                    self.log.error(
                        "Command '{}' timed out after {} seconds".format(
                            self.cmd, self.timeout)
                    )
                    raise TimeoutExpired(self.cmd, self.timeout)
                time.sleep(0.1)  # CPU 부하를 줄이기 위해 대기

            stdout, stderr = sub_pro.communicate()
            # self.log.info(f'[SubProcess] stdout : {stdout}')
            # self.log.info(f'[SubProcess] stderr : {stderr}')
            return stdout, stderr
        except Exception as e:
            self.log.error("An error occurred while executing '{}': {}".format(
                self.cmd, str(e))
            )
            self.log.error(traceback.format_exc())
            return None, None

