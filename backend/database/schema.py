from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship

from .database import Base

import uuid


# class ModelBase(Base):

#     __abstract__ = True

#     id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    # created_at = Column(DateTime, default=db.func.current_timestamp())
    # updated_at = Column(DateTime,
    #                 default=func.current_timestamp(),
    #                 onupdate=func.current_timestamp())

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True)
    encrypted_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")

    # def set_password(self, password):
    #     self.encrypted_password = bc.generate_password_hash(password)

    # def verify_password(self, password):
    #     return bc.check_password_hash(self.encrypted_password, password)
    def __str__(self):
        return f"<User {self.email}>"

    def __repr__(self):
        return f"<User {self.email}>"


class Item(Base):
    __tablename__ = "items"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    title = Column(String)
    description = Column(String)
    owner_id = Column(String, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")

# region 记忆单词相关
class UserBook(Base):
    __tablename__ = "user_book"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    owner_id = Column(String, ForeignKey("users.id"))
    book_id = Column(String, ForeignKey("book.bk_id"))

    title = Column(String)
    batch_size = Column(Integer, default=10)
    random = Column(Boolean, default=True)
    memorizing_batch = Column(String, default='')

class UserMemoryBatch(Base):
    __tablename__ = "user_memory_batch"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    user_book_id = Column(String, ForeignKey("user_book.id"))

    story = Column(String, default="")
    translated_story = Column(String, default="")
    words = relationship("UserMemoryWord", back_populates="batch")


class UserMemoryBatchAction(Base):
    __tablename__ = "user_memory_batch_action"
    """
    开始记忆到结束记忆的时间，可以计算记忆效率
    """

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    batch_id = Column(String, ForeignKey("user_memory_batch.id"))

    action = Column(String, default="start")  # start or end
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, onupdate=datetime.now, default=datetime.now)


class UserMemoryWord(Base):
    __tablename__ = "user_memory_word"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    batch_id = Column(String, ForeignKey("user_memory_batch.id"))
    word_id = Column(String, ForeignKey("word.vc_id"))

    batch = relationship("UserMemoryBatch", back_populates="words")
    actions = relationship("UserMemoryAction", back_populates="words")

class UserMemoryAction(Base):
    __tablename__ = "user_memory_action"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    user_memory_word_id = Column(String, ForeignKey("user_memory_word.id"))

    action = Column(String, default="remenber")  # remenber or forget
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, onupdate=datetime.now, default=datetime.now)

    words = relationship("UserMemoryWord", back_populates="actions")
# endregion

class BookSeries(Base):
    __tablename__ = "book_series"

    bk_series_id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    bk_level = Column(Integer)
    bk_order = Column(Float)
    bk_name = Column(String)
    bk_item_num = Column(Integer)
    bk_direct_item_num = Column(Integer)
    bk_author = Column(String, default='')
    bk_book = Column(String, default='')
    bk_comment = Column(String, default='')
    bk_organization = Column(String, default='')
    bk_publisher = Column(String, default='')
    bk_version = Column(String, default='')
    bk_flag = Column(String, default='')

    books = relationship("Book", back_populates="book_series")

    def __str__(self):
        return f"{self.bk_name}"
    def __repr__(self):
        return f"<BookSeries {self.bk_name}>"

class Book(Base):
    __tablename__ = "book"

#   {'bk_id': 'd645920e395fedad7bbbed0e',
#   'bk_parent_id': '6512bd43d9caa6e02c990b0a',
#   'bk_level': 2,
#   'bk_order': 2.0,
#   'bk_name': '人教版高中英语1 - 必修',
#   'bk_item_num': 315,
#   'bk_direct_item_num': 315,
#   'bk_author': '刘道义',
#   'bk_book': '人教版普通高中课程标准实验教科书 英语 1 必修',
#   'bk_comment': '黑体：本单元重点词汇和短语；无“△”：课标词汇，要求掌握；有“△”：不要求掌握（会出现大量缩写、人名、地名和短语，请选背）。',
#   'bk_organization': '人民教育出版社 课程教材研究所；英语课程教材研究开发中心',
#   'bk_publisher': '人民教育出版社',
#   'bk_version': '2007年1月第2版',
#   'bk_flag': '默认：152;黑体：97;前△：66'},
    bk_id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    bk_level = Column(Integer)
    bk_order = Column(Float)
    bk_name = Column(String)
    bk_item_num = Column(Integer)
    bk_direct_item_num = Column(Integer)
    bk_author = Column(String, default='')
    bk_book = Column(String, default='')
    bk_comment = Column(String, default='')
    bk_organization = Column(String, default='')
    bk_publisher = Column(String, default='')
    bk_version = Column(String, default='')
    bk_flag = Column(String, default='')

    book_series_id = Column(String, ForeignKey("book_series.bk_series_id"))
    book_series = relationship("BookSeries", back_populates="books")

    def __str__(self):
        return f"{self.bk_name}\n    [{self.bk_book} {self.bk_version}]"
    def __repr__(self):
        return f"<Book {self.bk_name}>"

class Unit(Base):
    __tablename__ = "unit"

    # ['bv_id', 'bv_book_id', 'bv_voc_id', 'bv_flag', 'bv_tag', 'bv_order']
#     {'bv_id': '58450c828958a37d5c10f763',
#   'bv_book_id': 'd645920e395fedad7bbbed0e',
#   'bv_voc_id': '57067b9ca172044907c615d7',
#   'bv_flag': 4,
#   'bv_tag': 'Unit 1',
#   'bv_order': 1},
    bv_id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    bv_voc_id = Column(String, ForeignKey("word.vc_id"))
    bv_book_id = Column(String, ForeignKey("book.bk_id"))
    bv_flag = Column(Integer)
    bv_tag = Column(String)
    bv_order = Column(Integer)

class Word(Base):
    __tablename__ = "word"

    # vc_id>vc_vocabulary>vc_phonetic_uk>vc_phonetic_us>vc_frequency>vc_difficulty>vc_acknowledge_rate
    # 57067c89a172044907c6698e>superspecies>[su:pərsˈpi:ʃi:z]>[supɚsˈpiʃiz]>0.0>1>0.664122
    vc_id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    vc_vocabulary = Column(String)
    vc_translation = Column(String)
    vc_phonetic_uk = Column(String)
    vc_phonetic_us = Column(String)
    vc_frequency = Column(Float)
    vc_difficulty = Column(Float)
    vc_acknowledge_rate = Column(Float)

    def __str__(self):
        return f"{self.vc_vocabulary} {self.vc_translation}\n[{self.vc_phonetic_uk}] [{self.vc_phonetic_us}]"

    def __repr__(self):
        return f"{self.vc_vocabulary} {self.vc_translation}\n[{self.vc_phonetic_uk}] [{self.vc_phonetic_us}]"
