#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""program"""
__author__ = "Jamongss"
__date__ = "2024-09-26"
__last_modified_by__ = "Jamongss"
__last_modified_date__ = "2025-10-01"
__maintainer__ = "Jamongss"

###########
# imports #
###########
import os
import sys
import docker
import traceback
from docker.errors import DockerException
from string_packages import StrPack

#########
# class #
#########
class CheckDocker:
    def __init__(self,
                 log,
                 container_list,
                 total_cnt = 0,
                 check_cnt = 0,
                 err_cnt = 0
                 ):
        self.log = log
        self.check_engine_list = container_list
        self.total_cnt = total_cnt
        self.check_cnt = check_cnt
        self.err_cnt = err_cnt
        self.cnt = len(self.check_engine_list)

    def run(self):
        if '' in self.check_engine_list:
            return self.total_cnt, self.check_cnt, self.err_cnt

        try:
            self.total_cnt += len(self.check_engine_list)
            container_list = list()
            container_dict = dict()

            self.log.info("{} [ Docker LIST ] {}".format('<' * 30, '>' * 31))
            # self.log.info('*' * 78)
            self.log.info('-' * 78)

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

                # self.log.info(container_list)
                # self.log.info(container_dict)

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
            # self.log.info("{}\n".format('*' * 78))
        except DockerException as e:
            self.log.error("Docker 예외 발생\n\t-> {}".format(e))
        except Exception:
            self.log.error(traceback.format_exc())
        finally:
            if self.total_cnt != self.check_cnt + self.err_cnt:
                self.err_cnt = self.err_cnt + self.cnt
            return self.total_cnt, self.check_cnt, self.err_cnt


