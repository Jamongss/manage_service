#!/usr/bin/python
# -*- coding:utf-8 -*-

"""program"""
__author__ = "Maum.Ai - Jamong"
__date__ = "creation: 2024-09-26, modification: 2024-11-18"

###########
# imports #
###########
import re
import sys
sys.path.append('../')
from cfg.config import CHECKConfig
from sub_process import SubProcess

#########
# class #
#########
class Svctl:
    def __init__(self, log, svc_list, total_cnt = 0, check_cnt = 0, err_cnt = 0):
        self.log = log
        self.svc_list = svc_list
        self.total_cnt = total_cnt
        self.check_cnt = check_cnt
        self.err_cnt = err_cnt

    def check_status(self):
        self.total_cnt += len(self.svc_list)
        running_status = ['RUNNING']
        service_list = list()
        service_dict = dict()

        self.log.info("{} [ SERVICE LIST ] {}\n".format('<' * 30, '>' * 30))
        self.log.info('*' * 78)
        self.log.info('-' * 78)

        cmd = "{} status".format(CHECKConfig.svctl_cmd)
        timeout = 60

        sub_proc = SubProcess(cmd, timeout)
        std_out, std_err = sub_proc.sub_process_popen()

        if std_out is None and std_err is None:
            # raise Exception ('\t[!! ERROR !!] svctl result is None')
            raise RuntimeError("\t[!! ERROR !!] svctl result is None for command: {}".format(cmd))

        if len(std_out) > 0:
            for result in std_out.strip().split('\n'):
                result = re.sub(r'\s+', ' ', result.strip())
                if len(result.strip().split(' ')) >= 1:
                    # result.split(' ') = ['stt-proxy', 'RUGGING', 'pid', '10487,', 'uptime', '37', 'days', '2:56:18']
                    if result.split(' ')[0] in self.svc_list:
                        service_name = result.split(' ')[0]
                        service_list.append(service_name)
                        service_status = result.split(' ')[1]
                        service_dict[service_name] = service_status

        for target in self.svc_list:
            if target in service_list:
                for status_code in running_status:
                    if status_code in service_dict[target]:
                        self.log.info("\t[  RUNNING  ]          ----->          {}".format(target))
                        self.check_cnt += 1
                        break
                    elif status_code not in service_dict[target]:
                        self.log.error("\t[!! ERROR !!]          ----->          {}".format(target))
                        self.err_cnt += 1
                        break
            else:
                self.log.error("\t[!! ERROR !!]        Not exists        {}".format(target))
                self.err_cnt += 1
        self.log.info('-' * 78)
        self.log.info("{}\n".format('*' * 78))
        
        return self.total_cnt, self.check_cnt, self.err_cnt

    def control(self, log, action):
        self.log.info("{} service ... {}".format(action.upper(), self.svc_list))
        self.log.info('*' * 100)

        for service in self.svc_list:
            cmd = "{} {} {}".format(CHECKConfig.svctl_cmd, action, service)
            timeout = 30

            self.log.info("\t--> Command: {}".format(cmd))

            sub_proc = SubProcess(cmd, timeout)
            std_out, std_err = sub_proc.sub_process_popen()

            if std_out is None and std_err is None:
                raise RuntimeError("\t[!! ERROR !!] svctl result is None for command: {}".format(cmd))

            if len(std_out.strip()) > 0:
                self.log.info("\t--> Standard out:")
                self.log.info(std_out.strip())
            if len(std_err.strip()) > 0:
                self.log.info("\t--> Standard err:")
                self.log.info(std_err.strip())
            self.log.info("\t--> Done ...")
            self.log.info("-" * 100)
