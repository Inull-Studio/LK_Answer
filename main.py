import sqlite3
import os

DB_NAME = 'lk.db'


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class LK:
    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name
        self.db = sqlite3.connect(self.db_name)
        self.db.row_factory = dict_factory
        self.db.execute(
            '''create table if not exists lk_question
            (id integer primary key,
            description text,
            answer text);''')
        self.db.commit()

    def search_keyword(self, keyword):
        try:
            res = self.db.execute(
                'select * from lk_question where description like "%'+str(keyword)+'%"').fetchall()
            if res:
                return res
            return False
        except sqlite3.OperationalError as e:
            print(e)

    def insert_question(self, description, answer):
        try:
            self.db.execute(
                f"insert into lk_question(id,description,answer) values(null,\"{description}\",\"{answer}\");")
            self.db.commit()
            return True
        except sqlite3.OperationalError as e:
            print(e)

    def delete_question(self, keyword):
        try:
            if len(self.db.execute('select * from lk_question where description like "%'+keyword+'%"').fetchall()) > 1:
                print('has two answer! please check keyword')
                return False
            self.db.execute(
                'delete from lk_question where description like "%'+keyword+'%"')
            self.db.commit()
            return True
        except sqlite3.OperationalError as e:
            print(e)

    def show_all_data(self):
        try:
            return self.db.execute('select * from lk_question;').fetchall()
        except sqlite3.OperationalError as e:
            print(e)


if __name__ == '__main__':
    lk = LK()
    # print(lk.insert_question(description='欢迎来到实力至上注意的教室中哪个人物没有被退学？', answer='小宫叶吾'))
    # print(lk.search_keyword('月'))
    print(lk.show_all_data())
    # lk.delete_question('月之都')
