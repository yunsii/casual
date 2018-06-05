import re, time
import pymysql
from json import dump, loads
from DBUtils.PooledDB import PooledDB


def dict2json(dict_, path_):
    """
    字典或字典列表序列化保存为格式化json文件
    :param dict_:
    :param path_:
    :return:
    """
    with open(path_, 'w', encoding='utf-8') as jf:  # 保存中文字符时 encoding 和 ensure_ascii 需要同时设置
        dump(dict_, jf, ensure_ascii=False, indent=4)


def json2dict(path_):
    """
    反序列化json文件为字典或字典列表
    :param path_:
    :return:
    """
    with open(path_, 'r', encoding="utf-8") as sf:
        dict_ = loads(sf.read())
    return dict_


def str_time2int(str_time):
    """
    转换时间字符串为时间戳
    :param str_time:
    :return:
    """
    datetime_list = re.split(r"[- :]", str_time)
    if len(datetime_list) == 3:
        return int(time.mktime(time.strptime(str_time, "%Y-%m-%d")))
    elif len(datetime_list) == 5:
        return int(time.mktime(time.strptime(str_time, "%Y-%m-%d %H:%M")))
    elif len(datetime_list) == 6:
        return int(time.mktime(time.strptime(str_time, "%Y-%m-%d %H:%M:%S")))


def cookie_str2json(str_):
    """
    请求头中cookie值保存到本地json文件
    :param str_:
    :return:
    """
    cookies_dict = dict()
    for i in str_.split(";"):
        j = i.strip().split("=")
        if len(j) == 3:
            cookies_dict[j[0]] = "{}={}".format(j[1], j[2])
        else:
            cookies_dict[j[0]] = j[1]
    dict2json(cookies_dict, "./json/cookies.json")


# ------------------------------------------------------------
#                      数据库相关
# ------------------------------------------------------------


def escape_db_string(str_):
    """
    数据库中字符串转义
    :param str_:
    :return:
    """
    symbols = [
        ("\\", r"\\"),
        (r"'", r"\'"),
        ("\n", r"\n")
    ]
    for i, j in symbols:
        str_ = str_.replace(i, j)
    return str_


def dict2replace_sql(dict_):
    """
    字典转换为replace语句
    :param dict_:
    :return:
    """
    table = dict_['table']
    # print(table)
    dict_.pop('table')
    kv_str = ''
    for k, v in dict_.items():
        kv_str = kv_str + k + ' = ' + "'" + str(v) + "', "
    insert_sql = 'REPLACE INTO ' + table + ' SET ' + kv_str
    insert_sql = insert_sql[:-2]
    return insert_sql


class MysqlUtil(object):
    __pool = None

    def __init__(self, host, user, passwd, db, port, charset):
        # 构造函数，创建数据库连接、游标
        self.conn = MysqlUtil.get_mysql_conn(self, host, user, passwd, db, port, charset)
        self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 数据库连接池连接
    def get_mysql_conn(self, host, user, passwd, db, port, charset):
        mysql_info = {
            "host": host,
            "user": user,
            "passwd": passwd,
            "db": db,
            "port": port,
            "charset": charset
        }
        if MysqlUtil.__pool is None:
            self.__pool = PooledDB(creator=pymysql, mincached=1, maxcached=20, host=mysql_info['host'],
                                   user=mysql_info['user'], passwd=mysql_info['passwd'], db=mysql_info['db'],
                                   port=mysql_info['port'], charset=mysql_info['charset'])
        return self.__pool.connection()

    def update_(self, sql):
        """
        执行一条更新语句 插入\更新\删除
        :param sql:
        :return:
        """
        insert_num = self.cur.execute(sql)
        self.conn.commit()
        return insert_num

    def batch_execute_sql(self, sql_list):
        """
        批量执行更新语句
        :param sql_list:
        :return:
        """
        insert_count = 0
        if isinstance(sql_list, str):
            sql_list = [sql_list]
        for sql in sql_list:
            # print(sql)
            insert_num = self.cur.execute(sql)
            insert_count += insert_num
        self.conn.commit()
        return insert_count

    def select_(self, sql):
        """
        执行一条查询语句
            查询结果为空时 results 类型为tuple
        :param sql:
        :return: 字典列表
        """
        self.cur.execute(sql)  # 执行sql
        results = self.cur.fetchall()
        if isinstance(results, tuple) and not results:
            results = list()
        return results

    def close(self):
        """
        释放资源
        :return:
        """
        self.conn.close()
        self.cur.close()


if __name__ == "__main__":
    # print(json2dict("./json/cookies.json"))
    escape_db_string("a\'b")
    pass
