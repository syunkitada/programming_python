import argparse
from datetime import datetime
from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine, select

parser = argparse.ArgumentParser()
parser.add_argument("action", help="action", type=str)
args = parser.parse_args()


class Mail(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    age: Optional[int] = None
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


sqlite_file_name = "/tmp/database.db"  # テーブル名
sqlite_url = f"sqlite:///{sqlite_file_name}"  # エンジンデータベースのURL

engine = create_engine(sqlite_url, echo=True)  # engineを作成


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)  # モデルからテーブルを生成


def create_mails():
    mail_1 = Mail(name="taro", email="taro@example.com", age=18)
    mail_2 = Mail(name="jiro", email="taro@example.com")
    mail_3 = Mail(name="saburo", email="taro@example.com", age=13)

    session = Session(engine)
    session.add(mail_1)  # 追加
    session.add(mail_2)  # 追加
    session.add(mail_3)  # 追加
    session.commit()


def select_mails():
    with Session(engine) as session:
        stmt = select(Mail)
        results = session.exec(stmt)
        for mail in results:
            print(mail)


def update():
    with Session(engine) as session:
        stmt1 = select(Mail).where(Mail.name == "taro")
        result1 = session.exec(stmt1)
        mail = result1.one()
        mail.age = 20  # 更新
        session.add(mail)  # 更新したデータをデータベース登録
        session.commit()  # データベースの中で永続化
        stmt2 = select(Mail).where(Mail.name == "taro")
        result2 = session.exec(stmt2)
        print("(update後)Mail: ", result2.one())


def delete():
    with Session(engine) as session:
        stmt1 = select(Mail).where(Mail.name == "taro")
        result1 = session.exec(stmt1)
        mail = result1.one()
        session.delete(mail)
        session.commit()


def main():
    if args.action == "init":
        create_db_and_tables()
        create_mails()
    elif args.action == "select":
        select_mails()
    elif args.action == "update":
        update()
    elif args.action == "delete":
        delete()
