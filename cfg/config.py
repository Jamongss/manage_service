#!/usr/bin/env python3
# -*- coding:utf-8 -*-

class MonitorConfig(object):
    logger_name = 'MONITORING_SERVICE'
    log_dir_path = 'logs/monitor_service'
    log_file_name = 'monitor_service.log'
    backup_count = 5
    log_level = 'debug'
    check_service_list = [
        'print_time', 'test_string'
    ]
    check_engine_list = [
        'former-jamong', 'haproxy2.5'
    ]
    check_process_list = ['sshd']
    svctl_cmd = "svctl"
    docker_cmd = "docker ps -a --format '{{.Status}}\t{{.Names}}'"

class RestartConfig(object):
    logger_name = 'RESTART_SERVICE'
    log_dir_path = 'logs/restart'
    log_file_name = 'restart_service.log'
    backup_count = 8
    log_level = 'info'
    service_list = ['print_time']

class DELConfig(object):
    logger_name = 'DELETE_FILE'
    log_dir_path = 'logs/delete_file'
    log_file_name = 'delete_file.log'
    backup_count = 3
    log_level = 'debug'
    target_dict_list = [
                {
                 'directory_path': '/data/dev_area/jamong/manage_pack/manage_service/logs',
                 'delete_file_date': '180'
                }
                # {
                #  'directory_path': '/DATA/maum/rec',
                #  'delete_file_date': '250'
                # }
    ]

class SUBPROCESSConfig(object):
    logger_name = 'SUB_PROCESS'
    log_dir_path = 'logs/sub_process'
    log_file_name = 'sub_process.log'
    backup_count = 3
    log_level = 'info'

class ORAConfig(object):
    db_type = 'oracle'
    # host = '0.0.0.0'
    host_list = ['10.50.1.123', '10.50.1.321']
    user = 'jamong'
    password = '1234'
    # ps_path = '/DATA/manage/enc/.password'
    port = 1521
    service_name = 'ORCL'
    sid = 'ORCL'
    failover = True
    reconnect_interval = 10

class DeleteDbConfig(object):
    logger_name = 'DELETE_DB'
    log_dir_path = 'logs/delete_db'
    log_file_name = 'delete_db.log'
    backup_count = 5
    log_level = 'info'

