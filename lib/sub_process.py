#!/usr/bin/python
# -*- coding:utf-8 -*-

"""program"""
__author__ = "Maum.Ai - Jamong"
__date__ = "creation: 2024-10-13, modification: 2024-11-12"

import sys
import time
import traceback
import subprocess
sys.path.append('../')
from cfg.config import SUBPROCESSConfig
from logger import get_timed_rotating_logger

###########
# options #
###########
reload(sys)
sys.setdefaultencoding('utf-8')

#########
# class #
#########
class TimeoutExpired(Exception):
    def __init__(self, cmd, timeout):
        self.cmd = cmd
        self.timeout = timeout
        super(TimeoutExpired, self).__init__("Command '{}' timed out after {} seconds.".format(cmd, timeout))

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
            log_dir_path=SUBPROCESSConfig.log_dir_path,
            log_file_name=SUBPROCESSConfig.log_file_name,
            backup_count=SUBPROCESSConfig.backup_count,
            log_level=SUBPROCESSConfig.log_level
        )
        return log

    def sub_process_popen(self):
        try:
            # subprocess.Popen을 사용하여 process 시작
            sub_pro = subprocess.Popen(self.cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            s_time = time.time()

            # timeout 체크
            while sub_pro.poll() is None:
                if time.time() - s_time >= self.timeout:
                    # timeout 발생 시 process 종료
                    sub_pro.kill()
                    self.log.error("Command '{}' timed out after {} seconds".format(self.cmd, self.timeout))
                    raise TimeoutExpired(self.cmd, self.timeout)
                time.sleep(0.1)  # CPU 부하를 줄이기 위해 대기

            stdout, stderr = sub_pro.communicate()
            # self.log.info(f'[SubProcess] stdout : {stdout}')
            # self.log.info(f'[SubProcess] stderr : {stderr}')
            return stdout, stderr
        except Exception as e:
            self.log.error("An error occurred while executing '{}': {}".format(self.cmd, str(e)))
            self.log.error(traceback.format_exc())
            return None, None
