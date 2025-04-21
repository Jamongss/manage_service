#!/usr/bin/python
# -*- coding:utf-8 -*-

"""program"""
__author__ = "Maum.Ai - Jamong"
__date__ = "creation: 2024-09-26, modification: 2024-11-18"

###########
# imports #
###########
import sys
from sub_process import SubProcess

###########
# options #
###########
reload(sys)
sys.setdefaultencoding('utf-8')

#########
# class #
#########
class CheckSystemctl:
    def __init__(self, log, sys_list, total_cnt = 0, check_cnt = 0, err_cnt = 0):
        self.log = log
        self.sys_list = sys_list
        self.total_cnt = total_cnt
        self.check_cnt = check_cnt
        self.err_cnt = err_cnt

    def run(self):
        self.total_cnt += len(self.sys_list)
        running_status = ['running']
        system_list = list()
        system_dict = dict()

        for target in self.sys_list:
            self.log.info("{} [ SYSTEM SERVICE LIST ] {}\n".format('<' * 26, '>' * 27))
            self.log.info('*' * 78)
            self.log.info('-' * 78)

            cmd = "systemctl status {}".format(target)
            timeout = 60

            sub_proc = SubProcess(cmd, timeout)
            std_out, std_err = sub_proc.sub_process_popen()

            if len(std_out) > 0:
                for result in std_out.split('\n'):
                    if running_status[0] in result:
                        system_list.append(target)
                        service_name = target
                        service_status = running_status[0]
                        system_dict[service_name] = service_status

        for target in self.sys_list:
            if target in system_list:
                for running_code in running_status:
                    if 'running' in system_dict[target]:
                        self.log.info("\t[  RUNNING  ]          ----->          {}".format(target))
                        self.check_cnt += 1
                        break
                    elif running_code not in system_dict[target]:
                        self.log.error("\t[!! ERROR !!]          ----->          {}".format(target))
                        self.err_cnt += 1
                        break
            else:
                self.log.error("\t[!! ERROR !!]        Not exists        {}".format(target))
                self.err_cnt += 1
        self.log.info('-' * 78)
        self.log.info("{}\n".format('*' * 78))

        return self.total_cnt, self.check_cnt, self.err_cnt
