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

    def search_keyword(self, keyword, all: bool = False) -> list:
        try:
            if all:
                res = self.db.execute(
                    'select * from lk_question where description like "%'+str(keyword)+'%"').fetchall()
            else:
                res = self.db.execute(
                    'select answer from lk_question where description like "%'+str(keyword)+'%"').fetchall()
            if res:
                return res
            return False
        except sqlite3.OperationalError as e:
            print(e)

    def insert_question(self, description, answer) -> bool:
        try:
            self.db.execute(
                f"insert into lk_question(id,description,answer) values(null,\"{description}\",\"{answer}\");")
            self.db.commit()
            return True
        except sqlite3.OperationalError as e:
            print(e)

    def delete_question(self, keyword) -> bool:
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

    def change_question(self, id, description, answer) -> bool:
        try:
            self.db.execute(
                f'update lk_question set description="{description}",answer="{answer}" where id={id}')
            self.db.commit()
            return True
        except sqlite3.OperationalError as e:
            print(e)

    def show_all_data(self) -> list:
        try:
            return self.db.execute('select * from lk_question').fetchall()
        except sqlite3.OperationalError as e:
            print(e)

    def show_all_empty(self) -> list:
        try:
            return self.db.execute('select * from lk_question where description="" or answer=""').fetchall()
        except sqlite3.OperationalError as e:
            print(e)


if __name__ == '__main__':
    lk = LK()
    print(lk.insert_question(
        description='轻小说《黑之魔王》中以黑乃真央组成的冒险者小队叫什么？', answer='元素支配者'))
    # print(lk.search_keyword('黑幕'))
    # print(lk.show_all_data())
    # lk.delete_question('月之都')
    # lk.change_question(id=7, description='', answer='')
    # print(lk.show_all_data())
