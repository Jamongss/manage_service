#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""program"""
__author__ = "Jamongss"
__date__ = "2025-09-27"
__last_modified_by__ = "Jamongss"
__last_modified_date__ = "2025-10-01"
__maintainer__ = "Jamongss"

###########
# imports #
###########
import sys
import psutil
import traceback
from string_packages import StrPack

#########
# class #
#########
class CheckProcess:
    def __init__(self, log, proc_list,
                 total_cnt = 0, check_cnt = 0, err_cnt = 0):
        self.log = log
        self.check_proc_list = proc_list
        self.total_cnt = total_cnt
        self.check_cnt = check_cnt
        self.err_cnt = err_cnt

    def run(self):
        if '' in self.check_proc_list:
            return self.total_cnt, self.check_cnt, self.err_cnt

        """서비스 실행 상태 확인"""
        try:
            self.total_cnt += len(self.check_proc_list)
            for proc_name in self.check_proc_list:
                self.log.info(
                    "{} [ PROCESS LIST ] {}".format('<' * 30, '>' * 30)
                )
                self.log.info('{}'.format('-' * 78))

                found = False
                for proc in psutil.process_iter(['name', 'cmdline', 'ppid']):
                    try:
                        name = proc.info.get('name', '')
                        cmd = " ".join(proc.info.get('cmdline') or [])

                        # 프로세스 이름 또는 명령어에 포함되는지 확인
                        if proc_name in name or proc_name in cmd:
                            # master 프로세스 우선
                            if proc.info.get('ppid') == 1 or proc_name in name:
#                                self.log.info(
#                                    "[RUNNING] {} (PID={})".format(
#                                        proc_name, proc.pid)
#                                )
                                self.log.info(
                                    "{}{}".format(
                                        StrPack.RUNNING_STR, proc_name)
                                )
                                self.check_cnt += 1
                                found = True
                                break
                            else:
                                self.log.error(
                                    "{}{}".format(StrPack.ERR_STR, proc_name)
                                )
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue

                if not found:
                    self.log.error(
                        "{}{}".format(StrPack.NOT_EXISTS_STR, proc_name)
                    )
                    self.err_cnt += 1

            self.log.info('-' * 78)
            return self.total_cnt, self.check_cnt, self.err_cnt

        except Exception:
            self.log.error(traceback.format_exc())
            return self.total_cnt, self.check_cnt, self.err_cnt

