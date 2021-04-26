#!/usr/bin/env python
# coding:utf-8
import paramiko
import sshtunnel
import pymysql
import pandas as pd
import numpy as np
from datetime import date
from datetime import datetime


def downloadfrom_server(query_str, dbname="apollo_db"):
    """
    :param query_str:
    :param dbname:
    :return:
    """

    sql_hostname = "rm-uf68w63oscc91h0fh.mysql.rds.aliyuncs.com"
    sql_username = "erp_user_read"
    sql_password = "erp_user_read0401"

    sql_port = 3306

    ssh_host = "106.15.248.85"
    ssh_user = "root"
    ssh_port = 22
    ssh_pass = 'INsP%HdvhkhOr'
    start_date = datetime.now()

    with sshtunnel.SSHTunnelForwarder(
            (ssh_host, ssh_port),
            ssh_username=ssh_user,
            ssh_password=ssh_pass,
            remote_bind_address=(sql_hostname, sql_port)) as tunnel:
        conn = pymysql.connect(
            host='127.0.0.1',
            user=sql_username,
            passwd=sql_password,
            db=dbname,
            port=tunnel.local_bind_port
        )

        print('start to connect server\n')

        data = pd.read_sql_query(query_str, conn)

        print("day data shape: ", data.shape)

        print('done!\n')
        end_date = datetime.now()

        print(f"use time: {end_date - start_date}\n")
        conn.close()
        print(data)
        return data


downloadfrom_server("select id  from erc_waybill limit 1")
