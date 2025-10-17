#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""program"""
__author__ = "Jamongss"
__date__ = "2024-09-26"
__last_modified_by__ = "Jamongss"
__last_modified_date__ = "2025-10-17"
__maintainer__ = "Jamongss"

###########
# imports #
###########
import os
import sys
import traceback
sys.path.append('../')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from cfg.config import MonitorConfig
from sub_process import SubProcess
from string_packages import StrPack

#########
# class #
#########
class CheckDocker:
    def __init__(self,
                 log,
                 container_list,
                 py_ver = 3,
                 total_cnt = 0,
                 check_cnt = 0,
                 err_cnt = 0
                 ):
        self.log = log
        self.check_engine_list = container_list
        self.py_version = py_ver
        self.total_cnt = total_cnt
        self.check_cnt = check_cnt
        self.err_cnt = err_cnt
        self.cnt = len(self.check_engine_list)

    def py3_process(self):
        try:
            import docker
            from docker.errors import DockerException

            self.total_cnt += len(self.check_engine_list)
            container_list = list()
            container_dict = dict()

            """
            Call docker client list option
            all=False -> docker ps (default)
            all=True  -> docker ps -a
            """
            client = docker.from_env()
            containers = client.containers.list(all=True)

            for container in containers:
                name = container.name
                # status = container.status   # running exited
                # More than detailed status(ex: running, exited, created, dead...)
                detailed_status = container.attrs['State']['Status']
                container_dict[name] = detailed_status
                container_list.append(name)

                # self.log.debug(container_list)
                # self.log.debug(container_dict)

            for engine in self.check_engine_list:
                if engine in container_list:
                    if container_dict[engine]=='running':
                        self.log.info(
                            "{}{}".format(StrPack.RUNNING_STR, engine))
                        self.check_cnt += 1
                    else:
                        self.log.error("{}{}".format(StrPack.ERR_STR, engine))
                        self.err_cnt += 1
                else:
                    self.log.error("{}{}".format(StrPack.NOT_EXISTS_STR, engine))
                    self.err_cnt += 1
                self.cnt -= 1
            self.log.info('{}\n'.format('-' * 78))
        except Exception:
            self.log.error(traceback.format_exc())

    def py2_process(self):
        try:
            err_status = ['Exited', 'Restart', 'less than']

            self.total_cnt += len(self.check_engine_list)
            py2_container_list = list()
            py2_container_dict = dict()

            cmd = MonitorConfig.docker_cmd
            timeout = 10

            sub_proc = SubProcess(cmd, timeout)
            std_out, std_err = sub_proc.sub_process_popen()

            # self.log.debug("[CHECK_DOCKER] std_out: {}".format(std_out))

            if len(std_out) > 0:
                for result in std_out.split('\n'):
                    if len(result.split('\t')) == 2:
                        if result.split('\t')[1] in self.check_engine_list:
                            py2_container_list.append(result.split('\t')[1])
                            service_name = result.split('\t')[1]
                            service_status = result.split('\t')[0]
                            py2_container_dict[service_name] = service_status

            for engine in self.check_engine_list:
                if engine in py2_container_list:
                    for err_code in err_status:
                        if 'Up' in py2_container_dict[engine] and len(py2_container_dict[engine]) < 18:
                            self.log.info(
                                "{}{}".format(StrPack.RUNNING_STR, engine))
                            self.check_cnt += 1
                            break
                        elif err_code not in py2_container_dict[engine]:
                            self.log.error("{}{}".format(StrPack.ERR_STR, engine))
                            self.err_cnt += 1
                            break
                else:
                    self.log.error("{}{}".format(StrPack.NOT_EXISTS_STR, engine))
                    self.err_cnt += 1
        except Exception:
            self.log.error(traceback.format_exc())

    def run(self):
        if '' in self.check_engine_list:
            return self.total_cnt, self.check_cnt, self.err_cnt

        try:
            # self.log.debug("[CHECK_DOCKER] Python Version: {}".format(self.py_version))
            self.log.info("{} [ Docker LIST ] {}".format('<' * 30, '>' * 31))
            self.log.info('-' * 78)

            if self.py_version == 3:
                self.py3_process()
            elif self.py_version == 2:
                self.py2_process()
            else:
                self.log.warn("Please check your Python version.")

            self.log.info('-' * 78)
            self.log.info("{}\n".format('*' * 78))

            return self.total_cnt, self.check_cnt, self.err_cnt
        except Exception:
            self.log.error(traceback.format_exc())
        finally:
            if self.total_cnt != self.check_cnt + self.err_cnt:
                self.err_cnt = self.err_cnt + self.cnt
            return self.total_cnt, self.check_cnt, self.err_cnt

