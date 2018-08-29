import re, time, requests
import pymysql, datetime
from json import dump, loads, dumps
from DBUtils.PooledDB import PooledDB
from configparser import ConfigParser


def sleep_(st):
    time.sleep(st)


# ------------------------------------------------------------
#                       对象相关
# ------------------------------------------------------------


def merge_dict(dict_, dict_another):
    """
    字典对象合并
    :param dict_:
    :param dict_another:
    :return:
    """
    return dict(dict_, **dict_another)


# ------------------------------------------------------------
#                       时间转换相关
# ------------------------------------------------------------


def get_int_time_now():
    """
    系统当前时间戳，以秒计
    :return:
    """
    return int(time.time())


def get_format_datetime_now():
    """
    格式化时间戳strftime && strptime
    :return:
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))


def str_time2int(str_time: str):
    """
    转换时间字符串为时间戳
    :param str_time:
    :return:
    """
    stamp = int()
    try:
        datetime_list = re.split(r"[- :]", str_time)
        datetime_list = [i for i in datetime_list if i]
        print(datetime_list)
        if len(datetime_list) == 3:
            stamp = int(time.mktime(time.strptime(str_time, "%Y-%m-%d")))
        elif len(datetime_list) == 5:
            stamp = int(time.mktime(time.strptime(str_time, "%Y-%m-%d %H:%M")))
        elif len(datetime_list) == 6:
            stamp = int(time.mktime(time.strptime(str_time, "%Y-%m-%d %H:%M:%S")))
        else:
            stamp = str_time
    except Exception as e:
        print("Exception str_time:", str_time)
        print(e)
    finally:
        return stamp


def int2str_time(stamp, tplt="normal"):
    """
    时间戳转格式化时间字符串
    :param stamp:
    :param tplt:
    :return:
    """
    if tplt == "short":
        tplt = "%Y-%m-%d"
    elif tplt == "normal":
        tplt = "%Y-%m-%d %H:%M:%S"
    elif tplt == "withoutSec":
        tplt = "%Y-%m-%d %H:%M"
    return datetime.datetime.fromtimestamp(stamp).strftime(tplt)

# ------------------------------------------------------------
#                     json conf 等文件相关
# ------------------------------------------------------------


def get_value_from_conf(file_path, section, option):
    """
    获取配置文件唯一值
    :param file_path:
    :param section:
    :param option:
    :return:
    """
    conf = ConfigParser()  # 实例化
    conf.read(file_path, "utf-8")
    return conf.get(section, option)


def dict2format_string(dict_, indent=4):
    """
    字典格式化输出字符串
    :param dict_:
    :param indent:
    :return:
    """
    return dumps(dict_, ensure_ascii=False, indent=indent)


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


def get_response(is_json=False, encoding_=None, **kwargs):
    """
    网页请求
    :param is_json:
    # :param params:  请求参数
    # :param data:  表单数据
    :param encoding_:
    :return:
    """
    try:
        res = requests.request(**kwargs)
        if encoding_:
            res.encoding = encoding_
        if is_json:
            return res.json()
        return res
    except Exception as e:
        print("Error", e)
        return ""


# ------------------------------------------------------------
#                      字符串相关
# ------------------------------------------------------------


def find_nums(str_):
    """
    查找字符串中的数字
    :param str_:
    :return: 数字字符串列表
    """
    return re.findall(r"\d+", str_)


def is_chinese(uchar):
    """
    判断一个unicode是否是汉字
    :param uchar:
    :return:
    """
    if u'\u4e00' <= uchar <= u'\u9fa5':
        return True
    else:
        return False


def mix_align_len(mix_str):
    """
    计算中英文混合字符串对齐长度
    :param mix_str:
    :return:
    """
    align_len = 0
    for i in mix_str:
        if is_chinese(i):
            align_len += 2
        else:
            align_len += 1
    return align_len


def zh_en_align(mix_str, len_):
    """
    中英文混合字符串右填充为len_长度的对齐字符串
    :param mix_str:
    :param len_:
    :return:
    """
    align_len = mix_align_len(mix_str)
    if len_ >= align_len:
        return "{}{}".format(mix_str, "_" * (len_ - align_len))
    else:
        return "len_ 过短"


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


def dict2replace_sql(dict_, table):
    """
    字典转换为replace语句
    :param dict_:
    :param table:
    :return:
    """
    # table = dict_['table']
    # # print(table)
    # dict_.pop('table')
    kv_str = ''
    kv_str = ", ".join(["{}='{}'".format(k, v) for k, v in dict_.items()])
    insert_sql = "REPLACE INTO {} SET {}".format(table, kv_str)
    return insert_sql


def dict2update_sql(dict_, table, where_condition):
    """
    字典转换为replace语句
    :param dict_:
    :param table:
    :param where_condition:
    :return:
    """
    # table = dict_['table']
    # # print(table)
    # dict_.pop('table')
    kv_str = ", ".join(["{}='{}'".format(k, v) for k, v in dict_.items()])
    update_sql = "UPDATE {} SET {} WHERE {}".format(table, kv_str, where_condition)
    return update_sql


def dict2insert_sql(table, dict_list):
    """
    字段转换为insert语句
    :param table:
    :param dict_list:
    :return:
    """
    if isinstance(dict_list, dict):
        dict_list = [dict_list]

    insert_tplt = "INSERT INTO {}({}) VALUES{}"
    keys = list(dict_list[0].keys())
    values = [list(map(str, list(x.values()))) for x in dict_list]
    values = ["{0}{1}{2}".format("('", "', '".join(x), "')") for x in values]
    return insert_tplt.format(table, ", ".join(keys), ", ".join(values))


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
        执行一条更新语句，包括无返回值存储过程
        插入\ 1 插入 2 重写
        更新\
        删除\
        建表
        :param sql:
        :return:
        """
        insert_num = -1
        try:
            insert_num = self.cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            print("Error: {}\nSQL: {}".format(e, sql))
        finally:
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
            try:
                insert_num = self.cur.execute(sql)
                insert_count += insert_num
            except Exception as e:
                print("Error: {}\nSQL: {}".format(e, sql))
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

    def call_proc(self, proc_name, out_count=0, **args):
        """
        执行存储过程
            无返回值存储过程可通过 update_() 直接调用
        :param proc_name:
        :param out_count:
        :param args:
        :return:
        """
        args = list(args.values())
        self.cur.callproc(proc_name, args)
        if out_count:
            out_args = ["@_{}_{} {}".format(proc_name, x, args[x]) for x in range(len(args) - out_count, len(args))]
            return self.select_("SELECT {}".format(", ".join(out_args)))
        return list()

    def close(self):
        """
        释放资源
        :return:
        """
        self.cur.close()
        self.conn.close()


if __name__ == "__main__":
    # print((datetime.datetime(2018, 8, 26, 19, 15, 8)).timestamp())
    print(dict2insert_sql("table", {"link": "977", "room_id": 777}))
    pass

