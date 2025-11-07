#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""program"""
__author__ = "Jamongss"
__date__ = "2024-05-10"
__last_modified_by__ = "Jamongss"
__last_modified_date__ = "2025-11-07"
__maintainer__ = "Jamongss"

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
                    "\t>>> time_since_creation: {}\tdelete_{}: {}".format(
                        self.time_since_creation, target_type, delete_file_path
                    )
                )
                if os.path.islink(delete_file_path):
                    os.remove(delete_file_path)
                elif os.path.isfile(delete_file_path):
                    os.remove(delete_file_path)
                elif os.path.isdir(delete_file_path):
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
                self.log.info('=' * 95)
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
                delete_file_date = int(
                    target_info_dict.get('delete_file_date'))
                w_ob = os.walk(target_dir_path, topdown=False)
                for dir_path, sub_dirs, files in w_ob:
                    if len(files) == 0 and len(sub_dirs) == 0:
                        if dir_path:
                            time_since_creation = (
                                    datetime.now() - datetime.fromtimestamp(
                                        os.path.getctime(dir_path))
                            ).days
                            if (
                                dir_path
                                and time_since_creation >= delete_file_date
                            ):
                                self.log.info('Empty directory')
                                self.del_garbage(dir_path, 'dir')
                                self.delete_dir_cnt += 1
                    for file_path in files:
                        target_path = os.path.join(dir_path, file_path)
                        self.time_since_creation = (
                                    datetime.now() - datetime.fromtimestamp(
                                        os.path.getctime(target_path))
                        ).days
                        if (
                            target_path
                            and self.time_since_creation >= delete_file_date
                        ):
                            self.del_garbage(target_path, 'file')
                            self.delete_file_cnt += 1
                        else:
                            self.log.debug(
                                "\t>>> time_since_creation: {}\t\
                                Not_subject_to_deletion: {}".format(
                                    self.time_since_creation, target_path
                                )
                            )

            proc_start_time, required_time = elapsed_time.run()

            # Pretty Summary Log
            self.log.info("=" * 95)
            self.log.info(" " * 30 + '[ D E L E T I O N   S U M M A R Y ]')
            self.log.info("=" * 95)
            self.log.info("  Total Deleted Files       : {:>10,}".format(
                self.delete_file_cnt))
            self.log.info("  Total Deleted Directories : {:>10,}".format(
                self.delete_dir_cnt))
            self.log.info("  Total Items Deleted       : {:>10,}".format(
                self.delete_file_cnt + self.delete_dir_cnt))
            self.log.info("-" * 95)
            self.log.info("  Process Start Time        : {}".format(
                proc_start_time))
            self.log.info("  Time Required             : {}".format(
                required_time))
            self.log.info("=" * 95)
        except Exception:
            self.log.error(traceback.format_exc())
            sys.exit(1)


########
# main #
########
if __name__ == "__main__":
    delete_file = DeleteFile()
    delete_file.run()

