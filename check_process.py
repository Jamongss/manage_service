#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""program"""
__author__ = "Jamong"
__date__ = "creation: 2024-09-26, modification: 2024-11-18"

###########
# imports #
###########
import os
import sys
import traceback
import psutil
from cfg.config import CHECKConfig
from lib.logger import get_timed_rotating_logger
from lib.control_svctl import Svctl
from lib.check_docker import CheckDocker
from lib.check_systemctl import CheckSystemctl

###########
# options #
###########
reload(sys)
sys.setdefaultencoding('utf-8')

###################
# global variable #
###################
manage_root = os.path.dirname(os.path.abspath(__file__))

#########
# class #
#########
class CheckService:
    def __init__(self):
        self.log = get_timed_rotating_logger(
            logger_name=CHECKConfig.logger_name,
            log_dir_path=os.path.join(manage_root, CHECKConfig.log_dir_path),
            log_file_name=CHECKConfig.log_file_name,
            backup_count=CHECKConfig.backup_count,
            log_level=CHECKConfig.log_level
        )

    def run(self):
        try:
            total_count = 0  # type: int
            check_count = 0  # type: int
            err_count = 0  # type: int

            check_service_list = CHECKConfig.check_service_list
            check_engine_list = CHECKConfig.check_engine_list
            check_system_list = CHECKConfig.check_system_list

            c_svctl = Svctl(
                self.log,
                svc_list=check_service_list,
                total_cnt=total_count,
                check_cnt=check_count,
                err_cnt=err_count,
            )
            total_cnt, check_cnt, err_cnt = c_svctl.check_status()

            c_docker = CheckDocker(
                self.log,
                container_list=check_engine_list,
                total_cnt=total_cnt,
                check_cnt=check_cnt,
                err_cnt=err_cnt,
            )
            total_cnt, check_cnt, err_cnt = c_docker.run()

#            c_systemctl = CheckSystemctl(
#                self.log,
#                sys_list=check_system_list,
#                total_cnt=total_cnt,
#                check_cnt=check_cnt,
#                err_cnt=err_cnt,
#            )
#            total_cnt, check_cnt, err_cnt = c_systemctl.run()

            try:
                for  
                    for proc in psutil.process_iter(['pid', 'name', 'status']):
                        if service_name.lower() in proc.info['name'].lower():
                            return {
                                'running': True,
                                'pid': proc.info['pid'],
                                'status': proc.info['status'],
                                'name': proc.info['name']
                            }
                        else:
                            return {'running': False}
                except Exception as e:
                return {'error': str(e)}


            self.log.info('*' * 78)
            self.log.info('-' * 78)
            self.log.info("대상 서비스 개수 : {}".format(total_cnt))
            self.log.info("정상 실행 중인 서비스 개수 : {}".format(check_cnt))
            self.log.info("비정상 실행 중인 서비스 개수 : {}".format(err_cnt))
            self.log.info('-' * 78)
            self.log.info('*' * 78)



      except Exception:
            err_str = traceback.format_exc()
            self.log.error(err_str)


if __name__ == "__main__":
    check_service = CheckService()
    check_service.run()
