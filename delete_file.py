#!/usr/bin/python
# -*- coding:utf-8 -*-

"""program"""
__author__ = "Maum.Ai - Jamong"
__date__ = "creation: 2024-05-10, modification: 2024-10-29"

###########
# imports #
###########
import os
import sys
import time
import shutil
import traceback
from datetime import datetime
from cfg.config import DELConfig
from lib.elapsed_time import ElapsedTime
from lib.logger import get_timed_rotating_logger

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
class DeleteFile:
    def __init__(self):
        # Set Logger
        self.log = get_timed_rotating_logger(
            logger_name=DELConfig.logger_name,
            log_dir_path=os.path.join(manage_root, DELConfig.log_dir_path),
            log_file_name=DELConfig.log_file_name,
            backup_count=DELConfig.backup_count,
            log_level=DELConfig.log_level
        )
        self.pro_st_tm = datetime.fromtimestamp(time.time())
        self.delete_dir_cnt = 0
        self.delete_file_cnt = 0
        self.time_since_creation = 0

    def del_garbage(self, delete_file_path, target_type):
        if os.path.exists(delete_file_path):
            # noinspection PyBroadException
            try:
                self.log.info(
                    "     >>> time_since_creation: {}\tdelete_{}: {}".format(
                        self.time_since_creation, target_type, delete_file_path
                    )
                )
                if os.path.islink(delete_file_path):
                    os.remove(delete_file_path)
                if os.path.isfile(delete_file_path):
                    os.remove(delete_file_path)
                if os.path.isdir(delete_file_path):
                    shutil.rmtree(delete_file_path)
            except Exception:
                # err_str = traceback.format_exc()
                self.log.error("Can't delete {}".format(delete_file_path))

    def run(self):
        try:
            # Set elapsed time
            elapsed_time = ElapsedTime()

            self.log.info('[S T A R T] Delete file process ...')

            target_dict_list = DELConfig.target_dict_list

            for target_info_dict in target_dict_list:
                self.log.info('=' * 150)
                self.log.info(
                    "retention_period : {}\ttarget_path : {}".format(
                        target_info_dict['delete_file_date'],
                        target_info_dict['directory_path']
                    )
                )
                # Delete file
                target_dir_path = str(target_info_dict.get('directory_path'))
                if target_dir_path[-1] == '/':
                    target_dir_path = target_dir_path[:-1]
                delete_file_date = int(target_info_dict.get('delete_file_date'))
                w_ob = os.walk(target_dir_path)
                for dir_path, sub_dirs, files in w_ob:
                    if len(files) == 0 and len(sub_dirs) == 0:
                        if dir_path:
                            time_since_creation = (
                                    datetime.now() - datetime.fromtimestamp(os.path.getctime(dir_path))).days
                            if dir_path and time_since_creation >= delete_file_date:
                                self.log.info('Empty directory')
                                self.del_garbage(dir_path, 'dir')
                                self.delete_dir_cnt += 1
                    for file_path in files:
                        target_path = os.path.join(dir_path, file_path)
                        self.time_since_creation = (
                                    datetime.now() - datetime.fromtimestamp(os.path.getctime(target_path))).days
                        if target_path and self.time_since_creation >= delete_file_date:
                            self.del_garbage(target_path, 'file')
                            self.delete_file_cnt += 1
#                       else:
#                           logger.info(
#                               "     >>> time_since_creation: {}\tNot_subject_to_deletion: {}".format(
#                                   time_since_creation, target_path
#                               )
#                           )

            proc_start_time, required_time = elapsed_time.run()
            self.log.info("[ E N D ] Start time = {}, The time required = {}".format(proc_start_time, required_time))
        except Exception:
            err_str = traceback.format_exc()
            self.log.error(err_str)
            sys.exit()


########
# main #
########
if __name__ == "__main__":
    delete_file = DeleteFile()
    delete_file.run()
