'''
Created on 2019年3月31日

@author: bkd
'''
import sqlite3
from .kdconfig import db_file

cs = None
def init_db():
    conn = sqlite3.connect(db_file)
    cs = conn.cursor()
    cs.execute("create table launch_item (id integer primary key NOT NULL,ico varchar(200),name varchar(50) UNIQUE NOT NULL,address varchar(250),type integer NOT NULL)")
    print("创建launch_item表成功")
def init_connection():
    conn = sqlite3.connect(db_file)
    return conn
def insert_launch_item(item):
    conn = init_connection()
    cs = conn.cursor()
    cs.execute("insert into launch_item (ico,name,url,type,session_id) values(?,?,?,?,?)",(item["ico"],item["name"],item["url"],item["type"], item["session_id"]))
    conn.commit()
def get_launch_item_list(session_id):
    conn = init_connection()
    cs = conn.cursor()
    cs.execute("select * from launch_item where session_id = '{}' and catelog_id is null".format(session_id))
    return cs.fetchall()
def delete_launch_item(item_name):
    conn = init_connection()
    cs = conn.cursor()
    cs.execute("delete from launch_item where name = '{}' ".format(item_name))
    conn.commit()
def tuple2dict_launch_item(t):
    return {"id":t[0],"ico":t[1],"name":t[2],"url":t[3],"type":t[4],"session_id":t[5]}
    
def update_launch_item(item):
    conn = init_connection()
    cs = conn.cursor()
    print("update item:" ,item)
    cs.execute("update launch_item set ico = ?, name = ?, url = ?, type = ?, session_id = ?, catelog_id = ? where id = ? ",(item["ico"],item["name"],item["url"],item["type"],item["session_id"], item["catelog_id"], item["id"]))
    conn.commit()

def insert_session_item(item):
    conn = init_connection()
    cs = conn.cursor()
    cs.execute("insert into session (name,type,picture,color) values(?,?,?,?)",(item["name"],item["type"],item["picture"],item["color"]))
    conn.commit()
def update_session_item(item):
    conn = init_connection()
    cs = conn.cursor()
    print("update session:" ,item)
    cs.execute("update session set  name = ?,  type = ? ,picture = ?,color = ? where id = ? ",(item["ico"],item["name"],item["picture"],item["type"],item["id"]))
    conn.commit()        
def get_session_list():
    conn = init_connection()
    cs = conn.cursor()
    cs.execute("select * from session")
    return cs.fetchall()
def tuple2dict_session(t):
    return {"id":t[0],"name":t[1],"type":t[2],"picture":t[3],"color":t[4]}
def update_session(item):
    conn = init_connection()
    cs = conn.cursor()
    print("update session:" ,item)
    cs.execute("update session set  name = ?, picture = ?, type = ?, color = ? where id = ? ",(item["name"],item["picture"],item["type"],item["color"], item["id"]))
    conn.commit()
def get_launch_item_list_by_catelog(catelog_id):
    conn = init_connection()
    cs = conn.cursor()
    cs.execute("select * from launch_item where catelog_id = '{}'".format(catelog_id))
    return cs.fetchall()
def delete_session(session_id):
    conn = init_connection()
    cs = conn.cursor()
    cs.execute("delete from session where id = '{}' ".format(session_id))
    cs.execute("delete from launch_item where session_id = '{}' ".format(session_id))
    conn.commit()