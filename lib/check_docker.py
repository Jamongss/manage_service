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
sys.path.append('../')
from cfg.config import CHECKConfig
from sub_process import SubProcess

#########
# class #
#########
class CheckDocker:
    def __init__(self, log, container_list,
                 total_cnt = 0, check_cnt = 0, err_cnt = 0):
        self.log = log
        self.container_list = container_list
        self.total_cnt = total_cnt
        self.check_cnt = check_cnt
        self.err_cnt = err_cnt

    def run(self):
        if '' in self.container_list:
            return self.total_cnt, self.check_cnt, self.err_cnt

        err_status = ['Exited', 'Restart', 'less than']

        self.total_cnt += len(self.container_list)
        engine_list = list()
        engine_dict = dict()

        cmd = CHECKConfig.docker_cmd
        timeout = 30

        sub_proc = SubProcess(cmd, timeout)
        std_out, std_err = sub_proc.sub_process_popen()

        if len(std_out) > 0:
            for result in std_out.split('\n'):
                if len(result.split('\t')) == 2:
                    if result.split('\t')[1] in self.container_list:
                        engine_list.append(result.split('\t')[1])
                        service_name = result.split('\t')[1]
                        service_status = result.split('\t')[0]
                        engine_dict[service_name] = service_status

        for target in self.container_list:
            if target in engine_list:
                for err_code in err_status:
                    if 'Up' in engine_dict[target] \
                            and len(engine_dict[target]) < 18:
                        self.log.info("RUNNING [{}]".format(target))
                        self.check_cnt += 1
                        break
                    elif err_code not in engine_dict[target]:
                        self.log.error("ERROR [{}]".format(target))
                        self.err_cnt += 1
                        break
            else:
                self.log.error("ERROR [{}]".format(target))
                self.err_cnt += 1
                break

        return self.total_cnt, self.check_cnt, self.err_cnt

