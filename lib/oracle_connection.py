#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""program"""
__author__ = "Jamongss"
__date__ = "2024-10-31"
__last_modified_by__ = "Jamongss"
__last_modified_date__ = "2025-09-27"
__maintainer__ = "Jamongss"

###########
# imports #
###########
import os
import sys
import time
import logging
import cx_Oracle
import traceback
from logger import get_timed_rotating_logger
from sub_process import SubProcess

###########
# options #
###########
reload(sys)
sys.setdefaultencoding('utf-8')

#########
# class #
#########
class OracleConnect(object):
    def __init__(self, log, conf):
        if isinstance(log, logging.Logger):
            self.log = log
        else:
            self.log = get_timed_rotating_logger(
                logger_name='ORACLE_CONNECTION',
                log_dir_path='./',
                log_file_name='ora_connection.log',
                backup_count=1,
                log_level='info'
            )
        self.conf = conf
        self.dsn_tns = None
        self.conn = None
        self.cursor = None
        self.set_timeout = 30

        # Try Connect
        for _ in range(0, 3):
            try:
                self.log.info('[DATABASE] Try connecting to {0} DB ...'.format(conf.db_type))
                if conf.db_type.upper() == 'ORACLE':
                    self.cursor = self.db_connect(False, self.conf.failover, self.conf.service_name, self.set_timeout)
                else:
                    raise Exception('Not Supported {0}'.format(conf.db_type))
                self.log.info('[DATABASE] Success connect to {0} DB'.format(conf.db_type))
                break
            except Exception:
                self.log.error(traceback.format_exc())
                self.log.error("[DATABASE] Can't connect db")
                time.sleep(20)
        if not self.cursor:
            raise Exception("[DATABASE] Can't connect db")

    def db_connect(self, host_reverse=False, failover=False, service_name='', set_timeout=10):
        os.environ['NLS_LANG'] = '.AL32UTF8'
        if failover:
            self.dsn_tns = '(DESCRIPTION = (ADDRESS_LIST= (FAILOVER = on)(LOAD_BALANCE = off)'
            if host_reverse:
                self.conf.host_list.reverse()
            for host in self.conf.host_list:
                self.dsn_tns += '(ADDRESS= (PROTOCOL = TCP)(HOST = {0})(PORT = {1}))'.format(host, self.conf.port)
            if service_name:
                self.dsn_tns += ')(CONNECT_DATA=(SERVICE_NAME={0})))'.format(service_name)
            else:
                self.dsn_tns += ')(CONNECT_DATA=(SID={0})))'.format(self.conf.sid)
        else:
            if service_name is not '':
                self.dsn_tns = cx_Oracle.makedsn(
                    self.conf.host,
                    self.conf.port,
                    service_name=self.conf.service_name
                )
            else:
                self.dsn_tns = cx_Oracle.makedsn(
                    self.conf.host,
                    self.conf.port,
                    sid=self.conf.sid
                )

        self.log.info('[DATABASE] dsn_tns: {0}'.format(self.dsn_tns))

        self.conn = cx_Oracle.connect(
            self.conf.user,
            self.conf.password,
            # self.openssl_dec(),
            self.dsn_tns,
            timeout=set_timeout
        )
        return self.conn.cursor()

    def openssl_dec(self):
        self.log.info('[DATABASE] OpenSSL Dec ...')
        cmd = "openssl enc -seed -d -a -in {0} -pass file:{1}".format(self.conf.pd, self.conf.ps_path)
        sub_process = SubProcess(cmd)
        std_out, std_err = sub_process.sub_process_popen()
        return std_out.strip()

    def disconnect(self):
        try:
            self.log.info('[DATABASE] Disconnect ...')
            self.cursor.close()
            self.conn.close()
        except Exception:
            raise Exception(traceback.format_exc())

    def check_alive(self):
        try:
            check_query = "SELECT 'TEST' FROM DUAL"
            self.cursor.execute(check_query)
        except cx_Oracle.DatabaseError:
            print(traceback.format_exc())
            time.sleep(self.conf.reconnect_interval)
            self.db_connect(host_reverse=True, failover=True, service_name=self.conf.service_name)
        except Exception:
            if 'InterfaceError' in traceback.format_exc():
                self.db_connect(host_reverse=True, failover=True, service_name=self.conf.service_name)

    def rows_to_dict_list(self):
        columns = [i[0] for i in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor]


########
# main #
########
if __name__ == '__main__':
    class ORAConfig(object):
        db_type = 'oracle'
        # host = '0.0.0.0'
        host_list = ['10.50.1.118', '10.50.1.118']
        user = 'jamong'
        password = 'Kiss1234'
        ps_path = '/DATA/manage/enc/.password'
        port = 1521
        service_name = 'ORCL'
        sid = 'ORCL'
        failover = True
        reconnect_interval = 10

    query = """
        SELECT
          'TEST'
        FROM
          DUAL
    """

    oracle = OracleConnect(None, ORAConfig)
    oracle.cursor.execute(query,)
    # oracle.cursor.execute(query, bind)

    result = oracle.rows_to_dict_list()

    for item in result:
        print item

    oracle.conn.commit()
    oracle.disconnect()

