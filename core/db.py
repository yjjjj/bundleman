# coding:utf-8


import os
import sqlite3


def run(db_path, db_name, lib_name, lib_path, lib_version):

    if not os.path.exists(db_path):
        os.mkdir(db_path)

    # 创建与数据库的链接(如果文件不存在会被自动创建）
    connection = sqlite3.connect(db_path.joinpath(db_name))

    # 创建一个游标 cursor
    cursor = connection.cursor()

    # 创建表BundleManInfo(空表没有数据)
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS BundleManInfo
                    (
                     库名称 TEXT UNIQUE,
                     库路径 TEXT,
                     库版本 TEXT)
                   ''')

    # 插入单条数据
    data = "('{}', '{}', '{}')".format(lib_name, lib_path, lib_version)
    cursor.execute(f"INSERT OR REPLACE INTO BundleManInfo VALUES {data}")

    # 查询表数据
    # records = cursor.execute("SELECT * FROM BundleManInfo")
    # for record in records:
    #     print(record)

    connection.commit()  # 提交修改
    cursor.close()       # 关闭游标
    connection.close()   # 关闭连接


# path = Path("C:/Users/liujj/Documents/test")
# run(path, "bbb.db", "111", "222")


# 查询表数据
def check(db_path):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    records = cursor.execute("SELECT * FROM BundleManInfo")

    return records


