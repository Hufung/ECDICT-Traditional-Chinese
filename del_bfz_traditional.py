import csv
import sqlite3
from pathlib import Path, PurePath

import stardict

MYSQLITE = 'ecdictSqlite.db'


def new_inflection(exchange):
    """去除ECDICT exchange字段中冗餘的f:複數， b:比較級， z:最高級。如果與對應標
    籤內容不同，則予以保留。

    Note:
        ecdict exchange列中0: 代表Lemma，如 perceived 的 Lemma 是 perceive

        類型 	說明
        p 	過去式（did）
        d 	過去分詞（done）
        i 	現在分詞（doing）
        3 	第三人稱單數（does）
        r 	形容詞比較級（-er）
        t 	形容詞最高級（-est）
        s 	名詞複數形式
        0 	Lemma，如 perceived 的 Lemma 是 perceive
        1 	Lemma 的變換形式，比如 s 代表 apples 是其 lemma 的複數形式

        https://github.com/skywind3000/ECDICT/issues/23

    """

    if len(exchange) == 0:
        return ''
    lists = exchange.split('/')

    inflection = {}

    for trans in lists:
        inflection[trans[0]] = trans[2:]

    old_new = {'b': 'r', 'z': 't', 'f': 's'}
    # 只去除相應重複值。如不重複的話，仍保留b, z, f標籤。
    for i in old_new:
        if inflection.get(i):
            if not inflection.get(old_new[i]):
                inflection[old_new[i]] = inflection[i]
                inflection.pop(i)
            elif inflection[old_new[i]] == inflection[i]:
                inflection.pop(i)

    newexchange = []
    for i in inflection:
        newexchange.append(i + ':' + inflection[i])

    return ('/').join(newexchange)


def init_ecdict_sqlite():

    stardict.convert_dict(MYSQLITE, 'ecdict.csv')
    con = sqlite3.connect(MYSQLITE)
    cur = con.cursor()

    # 查詢所有行的數據
    select_query = "SELECT word, exchange FROM stardict"
    cur.execute(select_query)
    rows = cur.fetchall()

    # 遍歷每一行，根據 word和exchange 的值更新新建列lemma
    for row in rows:
        word = row[0]
        exchange = row[1]

        inflection = new_inflection(exchange)

        update_query = "UPDATE stardict SET exchange = ? WHERE word = ?"
        cur.execute(update_query, (inflection, word))

    con.commit()
    con.close()


init_ecdict_sqlite()  # 只需運行一次，生成sqlite3 db文件

# 轉換SQLITE爲csv文件
stardict.convert_dict('ecdict.csv', MYSQLITE)
