#!/usr/bin/env python
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
import os
import re
import sys
import traceback
sys.path.append('../')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from cfg.config import MonitorConfig
from sub_process import SubProcess
from string_packages import StrPack

###################
# global variable #
###################
manage_service_path = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))
engn_root = os.path.join(os.path.dirname(manage_service_path), 'supervisor-kit')

#########
# class #
#########
class Svctl:
    def __init__(self, log, svc_list, py_ver = 'py3',
                 total_cnt = 0, check_cnt = 0, err_cnt = 0):
        self.log = log
        self.svc_list = svc_list
        self.py_version = py_ver
        self.total_cnt = total_cnt
        self.check_cnt = check_cnt
        self.err_cnt = err_cnt

    def check_status(self):
        if '' in self.svc_list:
            return self.total_cnt, self.check_cnt, self.err_cnt

        try:
            self.total_cnt += len(self.svc_list)
            running_status = ['RUNNING']
            service_list = list()
            service_dict = dict()

            cmd = "{} status".format(
                os.path.join(engn_root, MonitorConfig.svctl_cmd))
            timeout = 30

            self.log.info("supervisor cmd: {}\n".format(cmd))

            self.log.info("{} [ SVCTL LIST ] {}".format('<' * 30, '>' * 30))
            # self.log.info('*' * 78)
            self.log.info('-' * 78)

            sub_proc = SubProcess(cmd, timeout)

            if self.py_version == 2:
                std_out, std_err = sub_proc.sub_process_popen()
            if self.py_version == 3:
                std_out, std_err = sub_proc.sub_process_run()

            if std_out is None and std_err is None:
                raise RuntimeError("ERROR [{}]".format(cmd))

            if len(std_out) > 0:
                for result in std_out.strip().split('\n'):
                    result = re.sub(r'\s+', ' ', result.strip())
                    if len(result.strip().split(' ')) >= 1:
                        # result.split(' ') = [
                        #     'stt-proxy', 'RUGGING', 'pid', '10487,',
                        #     'uptime', '37', 'days', '2:56:18'
                        # ]
                        if result.split(' ')[0] in self.svc_list:
                            service_name = result.split(' ')[0]
                            service_list.append(service_name)
                            service_status = result.split(' ')[1]
                            service_dict[service_name] = service_status

            for target in self.svc_list:
                if target in service_list:
                    for status_code in running_status:
                        if status_code in service_dict[target]:
                            self.log.info(
                                "{}{}".format(StrPack.RUNNING_STR, target))
                            self.check_cnt += 1
                            break
                        elif status_code not in service_dict[target]:
                            self.log.error("{}{}".format(StrPack.ERR_STR, target))
                            self.err_cnt += 1
                            break
                else:
                    self.log.error("{}{}".format(StrPack.NOT_EXISTS_STR, target))
                    self.err_cnt += 1

            self.log.info("{}\n".format('-' * 78))
            # self.log.info("{}\n".format('*' * 78))

            return self.total_cnt, self.check_cnt, self.err_cnt
        except Exception:
            self.log.error(traceback.format_exc())
            return self.total_cnt, self.check_cnt, self.err_cnt

    def control(self, action):
        self.log.info("{} service ... {}".format(
            action.upper(), self.svc_list))
        self.log.info('*' * 100)

        svctl_cmd = "{}".format(
            os.path.join(engn_root, MonitorConfig.svctl_cmd))

        for service in self.svc_list:
            action_cmd = "{} {} {}".format(svctl_cmd, action, service)
            timeout = 30

            self.log.info("\t--> Command: {}".format(action_cmd))

            sub_proc = SubProcess(action_cmd, timeout)
            std_out, std_err = sub_proc.sub_process_run()

            if std_out is None and std_err is None:
                raise RuntimeError("ERROR [{}]".format(action_cmd))

            if len(std_out.strip()) > 0:
                self.log.info("\t--> Standard out:")
                self.log.info(std_out.strip())
            if len(std_err.strip()) > 0:
                self.log.info("\t--> Standard err:")
                self.log.info(std_err.strip())

