#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""program"""
__author__ = "Jamongss"
__date__ = "2025-08-19"
__last_modified_by__ = "Jamongss"
__last_modified_date__ = "2025-09-27"
__maintainer__ = "Jamongss"

###########
# imports #
###########
import sys
from sub_process import SubProcess
from string_packages import StrPack

#########
# class #
#########
class CheckSystemctl:
    def __init__(self, log, sys_list,
                 total_cnt = 0, check_cnt = 0, err_cnt = 0):
        self.log = log
        self.sys_list = sys_list
        self.total_cnt = total_cnt
        self.check_cnt = check_cnt
        self.err_cnt = err_cnt

    def run(self):
        if '' in self.sys_list:
            return self.total_cnt, self.check_cnt, self.err_cnt

        self.total_cnt += len(self.sys_list)
        running_status = 'running'
        system_list = list()
        system_dict = dict()

        for target in self.sys_list:
            cmd = "systemctl status {}".format(target)
            timeout = 30

            sub_proc = SubProcess(cmd, timeout)
            std_out, std_err = sub_proc.sub_process_popen()

            # Check systemctl status
            if len(std_out) > 0:
                for result in std_out.split('\n'):
                    if running_status in result:
                        system_list.append(target)
                        service_name = target
                        service_status = running_status
                        system_dict[service_name] = service_status

        # Print service status
        for service in self.sys_list:
            if service in system_list:
                for running_code in running_status:
                    if running_code in system_dict[service]:
                        self.log.info(
                            "{}{}".format(StrPack.RUNNING_STR, service)
                        )
                        self.check_cnt += 1
                        break
                    elif running_code not in system_dict[service]:
                        self.log.error("{}{}".format(StrPack.ERR_STR, service))
                        self.err_cnt += 1
                        break
            else:
                self.log.error("{}{}".format(StrPack.NOT_EXISTS_STR, service))
                self.err_cnt += 1

        return self.total_cnt, self.check_cnt, self.err_cnt

