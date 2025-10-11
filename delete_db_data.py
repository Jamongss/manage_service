#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""program"""
__author__ = "Jamongss"
__date__ = "2024-10-31"
__last_modified_by__ = "Jamongss"
__last_modified_date__ = "2024-11-12"
__maintainer__ = "Jamongss"

###########
# imports #
###########
import sys
import time
import traceback
from datetime import datetime, timedelta
from cfg.config import DeleteDbConfig, ORAConfig
from lib.logger import get_timed_rotating_logger
from lib.oracle_connection import OracleConnect
from lib.ora_util import OracleQuery
from lib.elapsed_time import ElapsedTime

###########
# options #
###########
reload(sys)
sys.setdefaultencoding('utf-8')

#########
# class #
#########
class DeleteData(object):
    def __init__(self):
        # Set logger
        self.log = get_timed_rotating_logger(
            logger_name=DeleteDbConfig.logger_name,
            log_dir_path=DeleteDbConfig.log_dir_path,
            log_file_name=DeleteDbConfig.log_file_name,
            backup_count=DeleteDbConfig.backup_count,
            log_level=DeleteDbConfig.log_level
        )

        # Set elapsed time
        self.elapsed_time = ElapsedTime()

        # Set variable
        self.pro_st_tm = datetime.fromtimestamp(time.time())
        self.tm_target_date = (datetime.now() - timedelta(days=1*1)).strftime('%Y-%m-%d %H:%M:%S')
        self.cs_target_date = (datetime.now() - timedelta(days=5*365)).strftime('%Y-%m-%d %H:%M:%S')
        self.db_type = ORAConfig.db_type
        self.db_conf = ORAConfig
        self.db = False

        # Connect Db
        self.db = OracleConnect(self.log, self.db_conf)

    def run(self):
        try:
            # Set ora_util
            oracle_query = OracleQuery(self.log, self.db)

            self.log.info('[ S T A R T ] >>>>>>>>>> Delete old data from DB')

            # TM data delete
            before_tm_meta_total = oracle_query.select_tb_tm_stt_rcdg_info()
            tm_target_meta_list = oracle_query.select_tb_tm_stt_rcdg_info(self.tm_target_date)
            # [{'RFILE_NAME': 'SENyMfUYPlWF.wav', 'REC_ID': 'hOqKuDDUDkXd'}, ....]

            self.log.info('[TM] Target point: {}'.format(self.tm_target_date))
            self.log.info('1. TB_TM_STT_RCDG_INFO Before count  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            self.log.info('\t1-1. TM Record data count: {}'.format(len(before_tm_meta_total)))
            self.log.info('\t1-2. TM target meta data count: {}'.format(len(tm_target_meta_list)))
            self.log.info('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

            before_tm_rst_cnt = oracle_query.select_count_tb_tm_stt_rst()

            self.log.info('2. TB_TM_STT_RST Before count >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            self.log.info('\t2-1. Before TM STT result data count: {}'.format(before_tm_rst_cnt))
            self.log.info('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

            self.log.info('3. Start TM data delete ... >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            self.log.info('\t3-1. Delete TM STT Result ...')
            oracle_query.delete_tb_tm_stt_rst(self.tm_target_date)
            self.log.info('\t3-2. Delete TM REC Info ...')
            oracle_query.delete_tb_tm_stt_rcdg_info(self.tm_target_date)

            self.log.info('4. Delete TM data complete >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

            after_tm_meta_total = oracle_query.select_tb_tm_stt_rcdg_info()
            after_tm_rst_cnt = oracle_query.select_count_tb_tm_stt_rst()

            self.log.info('5. TM_STT_RST_TB After count  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            self.log.info('\t5-1. After TM Record data count: {}'.format(len(after_tm_meta_total)))
            self.log.info('\t5-2. After TM STT result data count: {}'.format(after_tm_rst_cnt))
            self.log.info('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

            # TM Statistics
            delete_tm_meta_cnt = len(before_tm_meta_total) - len(after_tm_meta_total)
            delete_tm_rst_cnt = before_tm_rst_cnt[0]['COUNT(*)'] - after_tm_rst_cnt[0]['COUNT(*)']
            self.log.info('TM REC meta delete count = {}'.format(delete_tm_meta_cnt))
            self.log.info('TM STT result delete count = {}'.format(delete_tm_rst_cnt))

            # -------------------------------------------------------------------------------------------------------- #
            # CS data delete
            before_cs_meta_total = oracle_query.select_tb_cs_stt_rcdg_info()
            cs_target_meta_list = oracle_query.select_tb_cs_stt_rcdg_info(self.cs_target_date)
            # [{'RFILE_NAME': 'SENyMfUYPlWF.wav', 'REC_ID': 'hOqKuDDUDkXd'}, ....]

            self.log.info('[CS] Target point: {}'.format(self.cs_target_date))
            self.log.info('1. TB_CS_STT_RCDG_INFO Before count  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            self.log.info('\t1-1. CS Record data count: {}'.format(len(before_cs_meta_total)))
            self.log.info('\t1-2. CS target meta data count: {}'.format(len(cs_target_meta_list)))
            self.log.info('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

            before_cs_rst_cnt = oracle_query.select_count_tb_cs_stt_rst()

            self.log.info('2. TB_CS_STT_RST Before count >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            self.log.info('\t2-1. Before CS STT result data count: {}'.format(before_cs_rst_cnt))
            self.log.info('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

            self.log.info('3. Start CS data delete ... >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            self.log.info('\t3-1. Delete CS STT Result ...')
            oracle_query.delete_tb_cs_stt_rst(self.cs_target_date)
            self.log.info('\t3-2. Delete CS REC Info ...')
            oracle_query.delete_tb_cs_stt_rcdg_info(self.cs_target_date)

            self.log.info('4. Delete CS data complete >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

            after_cs_meta_total = oracle_query.select_tb_cs_stt_rcdg_info()
            after_cs_rst_cnt = oracle_query.select_count_tb_cs_stt_rst()

            self.log.info('5. CS_STT_RST_TB After count  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            self.log.info('\t5-1. After CS Record data count: {}'.format(len(after_cs_meta_total)))
            self.log.info('\t5-2. After CS STT result data count: {}'.format(after_cs_rst_cnt))
            self.log.info('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

            # CS Statistics
            delete_cs_meta_cnt = len(before_cs_meta_total) - len(after_cs_meta_total)
            delete_cs_rst_cnt = before_cs_rst_cnt[0]['COUNT(*)'] - after_cs_rst_cnt[0]['COUNT(*)']
            self.log.info('CS REC meta delete count = {}'.format(delete_cs_meta_cnt))
            self.log.info('CS STT result delete count = {}'.format(delete_cs_rst_cnt))

            # Disconnect DB
            self.db.disconnect()

            proc_start_time, required_time = self.elapsed_time.run()
            self.log.info("[ E N D ] Start time = {}, The time required = {}".format(
                proc_start_time, required_time)
            )
        except Exception:
            err_str = traceback.format_exc()
            self.log.error(err_str)
            if self.db:
                self.db.disconnect()
            proc_start_time, required_time = self.elapsed_time.run()
            self.log.error("[Exception E N D] Start time = {}, The time required = {}".format(
                proc_start_time, required_time)
            )
        except KeyboardInterrupt:
            if self.db:
                self.db.disconnect()
            proc_start_time, required_time = self.elapsed_time.run()
            self.log.error("[KeyboardInterrupt E N D] Start time = {}, The time required = {}".format(
                proc_start_time, required_time)
            )

########
# main #
########
if __name__ == '__main__':
    delete_db = DeleteData()
    delete_db.run()
