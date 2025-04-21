#!/usr/bin/python
# -*- coding: utf-8 -*-

"""program"""
__author__ = "Maum.Ai - Jamong"
__date__ = "creation: 2024-10-29, modification: 2024-11-12"

###########
# imports #
###########
import sys
import time
import pymysql
import traceback
from sub_process import SubProcess

###########
# options #
###########
reload(sys)
sys.setdefaultencoding('utf-8')

#########
# class #
#########
class MYSQL(object):
    def __init__(self, conf):
        self.conf = conf
        self.conn = pymysql.connect(
            host=self.conf.host,
            user=self.conf.user,
            passwd=self.openssl_dec(),
            db=self.conf.database,
            port=self.conf.port,
            charset=self.conf.charset,
            connect_timeout=self.conf.connect_timeout,
            autocommit=True,
        )
        self.conn.autocommit(True)
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)

    def openssl_dec(self):
        cmd = "openssl enc -seed -d -a -in {0} -pass file:{1}".format(self.conf.pd, self.conf.ps_path)
        sub_process = SubProcess(cmd)
        std_out, std_err = sub_process.sub_process_popen()
        return std_out.strip()

    def check_alive(self):
        try:
            self.cursor.execute("SELECT 'TEST' FROM DUAL")
        except pymysql.DatabaseError as e:
            time.sleep(self.conf.reconnect_interval)
            self.__init__(self.conf)

    def disconnect(self):
        try:
            self.cursor.close()
            self.conn.close()
        except Exception:
            raise Exception(traceback.format_exc())

    def rows_to_dict_list(self):
        columns = [i[0] for i in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor]


########
# main #
########
if __name__ == '__main__':
    class MYConfig(object):
        host = '0.0.0.0'
        host_list = ['0.0.0.0']
        user = 'minds'
        pd = '/stt_nas/Stt_Real/cfg/.mystt'
        ps_path = '/stt_nas/Stt_Real/cfg/.fubonhyundai'
        port = 3306
        charset = 'utf8'
        database = 'minds'
        connect_timeout = 5
        reconnect_interval = 10

    query = """
    """

    mysql = MYSQL(MYConfig)
    mysql.cursor.execute(query,)
    # result = mysql.cursor.fetchall()

    result = mysql.rows_to_dict_list()

    for item in result:
        print item

    mysql.conn.commit()
    mysql.disconnect()
