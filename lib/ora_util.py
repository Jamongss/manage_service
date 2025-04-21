#!/usr/bin/python
# -*- coding:utf-8 -*-

"""program"""
__author__ = "Maum.ai - Jamong"
__date__ = "Creation: 2024-10-31, Modification: 2024-11-12"

###########
# imports #
###########
import sys
import traceback

###########
# options #
###########
reload(sys)
sys.setdefaultencoding('utf-8')

#########
# class #
#########
class OracleQuery(object):
    def __init__(self, log, db):
        self.log = log
        self.db = db

    def rows_to_dict_list(self):
        columns = [i[0] for i in self.db.cursor.description]
        return [dict(zip(columns, row)) for row in self.db.cursor]

    def select_tb_tm_stt_rcdg_info(self, tm_target_date = None):
        try:
            if tm_target_date is None:
                query = """
                  SELECT /*+ PARALLEL(TB_TM_STT_RCDG_INFO, 4) */
                        REC_ID,
                        RFILE_NAME
                  FROM
                        TB_TM_STT_RCDG_INFO
                """
                self.db.check_alive()
                self.db.cursor.execute(query)
            else:
                query = """
                    SELECT /*+ PARALLEL(TB_TM_STT_RCDG_INFO, 4) */
                        REC_ID,
                        RFILE_NAME
                    FROM
                        TB_TM_STT_RCDG_INFO
                    WHERE
                        RGST_DTM <= TO_DATE(:target_point, 'YYYY-MM-DD HH24:MI:SS')
                """
                bind = {
                    "target_point": tm_target_date
                }
                self.db.check_alive()
                self.db.cursor.execute(query, bind)
            result = self.rows_to_dict_list()
            if result is bool:
                return False
            if not result:
                return False
            return result
        except Exception:
            raise Exception(traceback.format_exc())

    def select_count_tb_tm_stt_rst(self):
        try:
            query = """
                SELECT /*+ PARALLEL(TB_TM_STT_RST, 4) */
                    count(*)
                FROM
                    TB_TM_STT_RST
            """
            self.db.check_alive()
            self.db.cursor.execute(query)
            result = self.rows_to_dict_list()
            if result is bool:
                return False
            if not result:
                return False
            return result
        except Exception:
            raise Exception(traceback.format_exc())

    def delete_tb_tm_stt_rcdg_info(self, tm_target_date):
        try:
            query = """
                DECLARE
                    rows_deleted NUMBER := 0;
                BEGIN
                    LOOP
                        DELETE FROM
                            TB_TM_STT_RCDG_INFO
                        WHERE
                            RGST_DTM < TO_DATE(:target_point, 'YYYY-MM-DD HH24:MI:SS')
                            AND ROWNUM <= 10000;
                
                        rows_deleted := SQL%ROWCOUNT;
                
                        COMMIT;
                
                        EXIT WHEN rows_deleted = 0;
                    END LOOP;
                END;
            """
            bind = {
                "target_point": tm_target_date
            }
            self.db.check_alive()
            self.db.cursor.execute(query, bind)
            self.db.conn.commit()
        except Exception:
            raise Exception(traceback.format_exc())

    def delete_tb_tm_stt_rst(self, tm_target_date):
        try:
            query = """
                DECLARE
                    rows_deleted NUMBER := 0;
                BEGIN
                    LOOP
                        DELETE FROM
                            TB_TM_STT_RST
                        WHERE
                            RGST_DTM < TO_DATE(:target_point, 'YYYY-MM-DD HH24:MI:SS')
                            AND ROWNUM <= 10000;
                
                        rows_deleted := SQL%ROWCOUNT;
                
                        COMMIT;
                
                        EXIT WHEN rows_deleted = 0;
                    END LOOP;
                END;
            """
            bind = {
                "target_point": tm_target_date
            }
            self.db.check_alive()
            self.db.cursor.execute(query, bind)
            self.db.conn.commit()
        except Exception:
            raise Exception(traceback.format_exc())

    def select_tb_cs_stt_rcdg_info(self, cs_target_date = None):
        try:
            if cs_target_date is None:
                query = """
                  SELECT /*+ PARALLEL(TB_CS_STT_RCDG_INFO, 4) */
                        REC_ID,
                        RFILE_NAME
                  FROM
                        TB_CS_STT_RCDG_INFO
                """
                self.db.check_alive()
                self.db.cursor.execute(query)
            else:
                query = """
                    SELECT /*+ PARALLEL(TB_CS_STT_RCDG_INFO, 4) */
                        REC_ID,
                        RFILE_NAME
                    FROM
                        TB_CS_STT_RCDG_INFO
                    WHERE
                        LST_CHG_DTM <= TO_DATE(:target_point, 'YYYY-MM-DD HH24:MI:SS')
                """
                bind = {
                    "target_point": cs_target_date
                }
                self.db.check_alive()
                self.db.cursor.execute(query, bind)
            result = self.rows_to_dict_list()
            if result is bool:
                return False
            if not result:
                return False
            return result
        except Exception:
            raise Exception(traceback.format_exc())

    def select_count_tb_cs_stt_rst(self):
        try:
            query = """
                SELECT /*+ PARALLEL(TB_CS_STT_RST, 4) */
                    count(*)
                FROM
                    TB_CS_STT_RST
            """
            self.db.check_alive()
            self.db.cursor.execute(query)
            result = self.rows_to_dict_list()
            if result is bool:
                return False
            if not result:
                return False
            return result
        except Exception:
            raise Exception(traceback.format_exc())

    def delete_tb_cs_stt_rcdg_info(self, cs_target_date):
        try:
            query = """
                DECLARE
                    rows_deleted NUMBER := 0;
                BEGIN
                    LOOP
                        DELETE FROM
                            TB_CS_STT_RCDG_INFO
                        WHERE
                            LST_CHG_DTM < TO_DATE(:target_point, 'YYYY-MM-DD HH24:MI:SS')
                            AND ROWNUM <= 10000;

                        rows_deleted := SQL%ROWCOUNT;

                        COMMIT;

                        EXIT WHEN rows_deleted = 0;
                    END LOOP;
                END;
            """
            bind = {
                "target_point": cs_target_date
            }
            self.db.check_alive()
            self.db.cursor.execute(query, bind)
            self.db.conn.commit()
        except Exception:
            raise Exception(traceback.format_exc())

    def delete_tb_cs_stt_rst(self, cs_target_date):
        try:
            query = """
                DECLARE
                    rows_deleted NUMBER := 0;
                BEGIN
                    LOOP
                        DELETE FROM
                            TB_CS_STT_RST
                        WHERE
                            RGST_DTM < TO_DATE(:target_point, 'YYYY-MM-DD HH24:MI:SS')
                            AND ROWNUM <= 10000;

                        rows_deleted := SQL%ROWCOUNT;

                        COMMIT;

                        EXIT WHEN rows_deleted = 0;
                    END LOOP;
                END;
            """
            bind = {
                "target_point": cs_target_date
            }
            self.db.check_alive()
            self.db.cursor.execute(query, bind)
            self.db.conn.commit()
        except Exception:
            raise Exception(traceback.format_exc())