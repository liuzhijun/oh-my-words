from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional, Tuple
from . import schema

# Pydantic models
class UserBase(BaseModel):
    email: str
    is_active: bool

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    hashed_password: Optional[str]  # This is optional because you may not always want to update the password

class User(UserBase):
    id: str

class ItemBase(BaseModel):
    title: str
    description: str

class ItemCreate(ItemBase):
    pass

class ItemUpdate(ItemBase):
    pass

class Item(ItemBase):
    id: str
    owner_id: str

# CRUD operations for User
def create_user(db: Session, user: UserCreate):
    db_user = schema.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: str):
    return db.query(schema.User).filter(schema.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(schema.User).filter(schema.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(schema.User).offset(skip).limit(limit).all()

def get_all_users(db: Session):
    return db.query(schema.User).all()

def update_user(db: Session, user_id: str, user: UserUpdate):
    db_user = db.query(schema.User).filter(schema.User.id == user_id).first()
    if db_user:
        for key, value in user.dict(exclude_unset=True).items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        return db_user

def delete_user(db: Session, user_id: str):
    db_user = db.query(schema.User).filter(schema.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return db_user

# CRUD operations for Item
def create_item(db: Session, item: ItemCreate, owner_id: str):
    db_item = schema.Item(**item.dict(), owner_id=owner_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_item(db: Session, item_id: str):
    return db.query(schema.Item).filter(schema.Item.id == item_id).first()

def get_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(schema.Item).offset(skip).limit(limit).all()

def update_item(db: Session, item_id: str, item: ItemUpdate):
    db_item = db.query(schema.Item).filter(schema.Item.id == item_id).first()
    if db_item:
        for key, value in item.dict(exclude_unset=True).items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
        return db_item

def delete_item(db: Session, item_id: str):
    db_item = db.query(schema.Item).filter(schema.Item.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
        return db_item

# Pydantic models for UserBook
class UserBookBase(BaseModel):
    owner_id: str
    book_id: str
    title: str
    random: bool
    batch_size: int
    memorizing_batch: str = ""

class UserBookCreate(UserBookBase):
    pass

class UserBookUpdate(UserBookBase):
    pass

class UserBook(UserBookBase):
    id: str

# CRUD operations for UserBook
def create_user_book(db: Session, user_book: UserBookCreate):
    db_user_book = schema.UserBook(**user_book.dict())
    db.add(db_user_book)
    db.commit()
    db.refresh(db_user_book)
    return db_user_book

def get_user_book(db: Session, user_book_id: str):
    return db.query(schema.UserBook).filter(schema.UserBook.id == user_book_id).first()

def get_user_books_by_owner_id(db: Session, owner_id: str):
    return db.query(schema.UserBook).filter(schema.UserBook.owner_id == owner_id).all()

def get_user_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(schema.UserBook).offset(skip).limit(limit).all()

def update_user_book(db: Session, user_book_id: str, user_book: UserBookUpdate):
    db_user_book = db.query(schema.UserBook).filter(schema.UserBook.id == user_book_id).first()
    if db_user_book:
        for key, value in user_book.dict(exclude_unset=True).items():
            setattr(db_user_book, key, value)
        db.commit()
        db.refresh(db_user_book)
        return db_user_book

def update_user_book_memorizing_batch(db: Session, user_book_id: str, memorizing_batch: str):
    db_user_book = db.query(schema.UserBook).filter(schema.UserBook.id == user_book_id).first()
    if db_user_book:
        db_user_book.memorizing_batch = memorizing_batch
        db.commit()
        db.refresh(db_user_book)
        return db_user_book

def delete_user_book(db: Session, user_book_id: str):
    db_user_book = db.query(schema.UserBook).filter(schema.UserBook.id == user_book_id).first()
    if db_user_book:
        db.delete(db_user_book)
        db.commit()
        return db_user_book

# Pydantic models for UserMemoryBatch
class UserMemoryBatchBase(BaseModel):
    user_book_id: str
    story: str
    translated_story: str

class UserMemoryBatchCreate(UserMemoryBatchBase):
    pass

class UserMemoryBatchUpdate(UserMemoryBatchBase):
    pass

class UserMemoryBatch(UserMemoryBatchBase):
    id: str

# CRUD operations for UserMemoryBatch
def create_user_memory_batch(db: Session, memory_batch: UserMemoryBatchCreate):
    db_memory_batch = schema.UserMemoryBatch(**memory_batch.dict())
    db.add(db_memory_batch)
    db.commit()
    db.refresh(db_memory_batch)
    return db_memory_batch

def get_user_memory_batch(db: Session, memory_batch_id: str):
    return db.query(schema.UserMemoryBatch).filter(schema.UserMemoryBatch.id == memory_batch_id).first()

def get_user_memory_batchs(db: Session, skip: int = 0, limit: int = 10):
    return db.query(schema.UserMemoryBatch).offset(skip).limit(limit).all()

def get_user_memory_batches_by_user_book_id(db: Session, user_book_id: str):
    return db.query(schema.UserMemoryBatch).filter(schema.UserMemoryBatch.user_book_id == user_book_id).all()

def update_user_memory_batch(db: Session, memory_batch_id: str, memory_batch: UserMemoryBatchUpdate):
    db_memory_batch = db.query(schema.UserMemoryBatch).filter(schema.UserMemoryBatch.id == memory_batch_id).first()
    if db_memory_batch:
        for key, value in memory_batch.dict(exclude_unset=True).items():
            setattr(db_memory_batch, key, value)
        db.commit()
        db.refresh(db_memory_batch)
        return db_memory_batch

def delete_user_memory_batch(db: Session, memory_batch_id: str):
    db_memory_batch = db.query(schema.UserMemoryBatch).filter(schema.UserMemoryBatch.id == memory_batch_id).first()
    if db_memory_batch:
        db.delete(db_memory_batch)
        db.commit()
        return db_memory_batch

# Pydantic models for UserMemoryBatchAction
class UserMemoryBatchActionBase(BaseModel):
    batch_id: str
    action: str

class UserMemoryBatchActionCreate(UserMemoryBatchActionBase):
    pass

class UserMemoryBatchActionUpdate(UserMemoryBatchActionBase):
    pass

class UserMemoryBatchAction(UserMemoryBatchActionBase):
    id: str
    create_time: str
    update_time: str

# CRUD operations for UserMemoryBatchAction
def create_user_memory_batch_action(db: Session, memory_batch_action: UserMemoryBatchActionCreate):
    db_memory_batch_action = schema.UserMemoryBatchAction(**memory_batch_action.dict())
    db.add(db_memory_batch_action)
    db.commit()
    db.refresh(db_memory_batch_action)
    return db_memory_batch_action

def get_user_memory_batch_action(db: Session, memory_batch_action_id: str):
    return db.query(schema.UserMemoryBatchAction).filter(schema.UserMemoryBatchAction.id == memory_batch_action_id).first()

def get_user_memory_batch_actions(db: Session, skip: int = 0, limit: int = 10):
    return db.query(schema.UserMemoryBatchAction).offset(skip).limit(limit).all()

def get_user_memory_batch_actions_by_user_memory_batch_id(db: Session, user_memory_batch_id: str):
    return db.query(schema.UserMemoryBatchAction).filter(schema.UserMemoryBatchAction.batch_id == user_memory_batch_id).all()

def get_actions_at_each_batch(db: Session, memory_batch_ids: List[str]):
    return db.query(schema.UserMemoryBatchAction).filter(schema.UserMemoryBatchAction.batch_id.in_(memory_batch_ids)).all()

def update_user_memory_batch_action(db: Session, memory_batch_action_id: str, memory_batch_action: UserMemoryBatchActionUpdate):
    db_memory_batch_action = db.query(schema.UserMemoryBatchAction).filter(schema.UserMemoryBatchAction.id == memory_batch_action_id).first()
    if db_memory_batch_action:
        for key, value in memory_batch_action.dict(exclude_unset=True).items():
            setattr(db_memory_batch_action, key, value)
        db.commit()
        db.refresh(db_memory_batch_action)
        return db_memory_batch_action

def delete_user_memory_batch_action(db: Session, memory_batch_action_id: str):
    db_memory_batch_action = db.query(schema.UserMemoryBatchAction).filter(schema.UserMemoryBatchAction.id == memory_batch_action_id).first()
    if db_memory_batch_action:
        db.delete(db_memory_batch_action)
        db.commit()
        return db_memory_batch_action

# Pydantic models for UserMemoryWord
class UserMemoryWordBase(BaseModel):
    batch_id: str
    word_id: str

class UserMemoryWordCreate(UserMemoryWordBase):
    pass

class UserMemoryWordUpdate(UserMemoryWordBase):
    pass

class UserMemoryWord(UserMemoryWordBase):
    id: str

# CRUD operations for UserMemoryWord
def create_user_memory_word(db: Session, memory_word: UserMemoryWordCreate):
    db_memory_word = schema.UserMemoryWord(**memory_word.dict())
    db.add(db_memory_word)
    db.commit()
    db.refresh(db_memory_word)
    return db_memory_word

def get_user_memory_word(db: Session, memory_word_id: str):
    return db.query(schema.UserMemoryWord).filter(schema.UserMemoryWord.id == memory_word_id).first()

def get_user_memory_words(db: Session, skip: int = 0, limit: int = 10):
    return db.query(schema.UserMemoryWord).offset(skip).limit(limit).all()

def get_user_memory_words_by_batch_id(db: Session, batch_id: str):
    return db.query(schema.UserMemoryWord).filter(schema.UserMemoryWord.batch_id == batch_id).all()

def update_user_memory_word(db: Session, memory_word_id: str, memory_word: UserMemoryWordUpdate):
    db_memory_word = db.query(schema.UserMemoryWord).filter(schema.UserMemoryWord.id == memory_word_id).first()
    if db_memory_word:
        for key, value in memory_word.dict(exclude_unset=True).items():
            setattr(db_memory_word, key, value)
        db.commit()
        db.refresh(db_memory_word)
        return db_memory_word

def delete_user_memory_word(db: Session, memory_word_id: str):
    db_memory_word = db.query(schema.UserMemoryWord).filter(schema.UserMemoryWord.id == memory_word_id).first()
    if db_memory_word:
        db.delete(db_memory_word)
        db.commit()
        return db_memory_word

# Pydantic models for UserMemoryAction
class UserMemoryActionBase(BaseModel):
    user_memory_word_id: str
    action: str

class UserMemoryActionCreate(UserMemoryActionBase):
    pass

class UserMemoryActionUpdate(UserMemoryActionBase):
    pass

class UserMemoryAction(UserMemoryActionBase):
    id: str
    create_time: str
    update_time: str

# CRUD operations for UserMemoryAction
def create_user_memory_action(db: Session, memory_action: UserMemoryActionCreate):
    db_memory_action = schema.UserMemoryAction(**memory_action.dict())
    db.add(db_memory_action)
    db.commit()
    db.refresh(db_memory_action)
    return db_memory_action

def get_user_memory_action(db: Session, memory_action_id: str):
    return db.query(schema.UserMemoryAction).filter(schema.UserMemoryAction.id == memory_action_id).first()

def get_user_memory_actions(db: Session, skip: int = 0, limit: int = 10):
    return db.query(schema.UserMemoryAction).offset(skip).limit(limit).all()

def get_user_memory_actions_by_user_memory_word_id(db: Session, user_memory_word_id: str):
    return db.query(schema.UserMemoryAction).filter(schema.UserMemoryAction.user_memory_word_id == user_memory_word_id).all()

def get_actions_at_each_word(db: Session, memory_word_ids: List[str]):
    return db.query(schema.UserMemoryAction).filter(schema.UserMemoryAction.user_memory_word_id.in_(memory_word_ids)).all()

def update_user_memory_action(db: Session, memory_action_id: str, memory_action: UserMemoryActionUpdate):
    db_memory_action = db.query(schema.UserMemoryAction).filter(schema.UserMemoryAction.id == memory_action_id).first()
    if db_memory_action:
        for key, value in memory_action.dict(exclude_unset=True).items():
            setattr(db_memory_action, key, value)
        db.commit()
        db.refresh(db_memory_action)
        return db_memory_action

def delete_user_memory_action(db: Session, memory_action_id: str):
    db_memory_action = db.query(schema.UserMemoryAction).filter(schema.UserMemoryAction.id == memory_action_id).first()
    if db_memory_action:
        db.delete(db_memory_action)
        db.commit()
        return db_memory_action

# Pydantic models for BookSeries
class BookSeriesBase(BaseModel):
    bk_level: int
    bk_order: float
    bk_name: str
    bk_item_num: int
    bk_direct_item_num: int
    bk_author: str
    bk_book: str
    bk_comment: str
    bk_organization: str
    bk_publisher: str
    bk_version: str
    bk_flag: str

class BookSeriesCreate(BookSeriesBase):
    pass

class BookSeriesUpdate(BookSeriesBase):
    pass

class BookSeries(BookSeriesBase):
    bk_series_id: str

# CRUD operations for BookSeries
def create_book_series(db: Session, book_series: BookSeriesCreate):
    db_book_series = schema.BookSeries(**book_series.dict())
    db.add(db_book_series)
    db.commit()
    db.refresh(db_book_series)
    return db_book_series

def get_book_series(db: Session, book_series_id: str):
    return db.query(schema.BookSeries).filter(schema.BookSeries.bk_series_id == book_series_id).first()

def get_book_series_list(db: Session, skip: int = 0, limit: int = 10):
    return db.query(schema.BookSeries).offset(skip).limit(limit).all()

def update_book_series(db: Session, book_series_id: str, book_series: BookSeriesUpdate):
    db_book_series = db.query(schema.BookSeries).filter(schema.BookSeries.bk_series_id == book_series_id).first()
    if db_book_series:
        for key, value in book_series.dict(exclude_unset=True).items():
            setattr(db_book_series, key, value)
        db.commit()
        db.refresh(db_book_series)
        return db_book_series

def delete_book_series(db: Session, book_series_id: str):
    db_book_series = db.query(schema.BookSeries).filter(schema.BookSeries.bk_series_id == book_series_id).first()
    if db_book_series:
        db.delete(db_book_series)
        db.commit()
        return db_book_series

# Pydantic models for Book
class BookBase(BaseModel):
    bk_id: str

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    pass

class Book(BookBase):
    bk_level: int
    bk_order: float
    bk_name: str
    bk_item_num: int
    bk_direct_item_num: int
    bk_author: str
    bk_book: str
    bk_comment: str
    bk_organization: str
    bk_publisher: str
    bk_version: str
    bk_flag: str
    book_series_id: str

# CRUD operations for Book
def create_book(db: Session, book: BookCreate, book_series_id: str):
    db_book = schema.Book(**book.dict(), book_series_id=book_series_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_book(db: Session, book_id: str):
    return db.query(schema.Book).filter(schema.Book.bk_id == book_id).first()

def get_book_by_name(db: Session, book_name: str):
    return db.query(schema.Book).filter(schema.Book.bk_name == book_name).first()

def get_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(schema.Book).offset(skip).limit(limit).all()

def get_all_books(db: Session):
    return db.query(schema.Book).all()

def update_book(db: Session, book_id: str, book: BookUpdate):
    db_book = db.query(schema.Book).filter(schema.Book.bk_id == book_id).first()
    if db_book:
        for key, value in book.dict(exclude_unset=True).items():
            setattr(db_book, key, value)
        db.commit()
        db.refresh(db_book)
        return db_book

def delete_book(db: Session, book_id: str):
    db_book = db.query(schema.Book).filter(schema.Book.bk_id == book_id).first()
    if db_book:
        db.delete(db_book)
        db.commit()
        return db_book

# Pydantic models for Unit
class UnitBase(BaseModel):
    bv_book_id: str
    bv_voc_id: str
    bv_flag: int
    bv_tag: str
    bv_order: int

class UnitCreate(UnitBase):
    pass

class UnitUpdate(UnitBase):
    pass

class Unit(UnitBase):
    pass

# CRUD operations for Unit
def create_unit(db: Session, unit: UnitCreate, book_id: str):
    db_unit = schema.Unit(**unit.dict(), bv_book_id=book_id)
    db.add(db_unit)
    db.commit()
    db.refresh(db_unit)
    return db_unit

def get_unit(db: Session, unit_id: str):
    return db.query(schema.Unit).filter(schema.Unit.bv_voc_id == unit_id).first()

def get_units(db: Session, skip: int = 0, limit: int = 10):
    return db.query(schema.Unit).offset(skip).limit(limit).all()

def update_unit(db: Session, unit_id: str, unit: UnitUpdate):
    db_unit = db.query(schema.Unit).filter(schema.Unit.bv_voc_id == unit_id).first()
    if db_unit:
        for key, value in unit.dict(exclude_unset=True).items():
            setattr(db_unit, key, value)
        db.commit()
        db.refresh(db_unit)
        return db_unit

def delete_unit(db: Session, unit_id: str):
    db_unit = db.query(schema.Unit).filter(schema.Unit.bv_voc_id == unit_id).first()
    if db_unit:
        db.delete(db_unit)
        db.commit()
        return db_unit

# Pydantic models for Word
class WordBase(BaseModel):
    vc_id: str
    vc_vocabulary: str
    vc_phonetic_uk: str
    vc_phonetic_us: str
    vc_frequency: float
    vc_difficulty: float
    vc_acknowledge_rate: float

class WordCreate(WordBase):
    pass

class WordUpdate(WordBase):
    pass

class Word(WordBase):
    pass

# CRUD operations for Word
def create_word(db: Session, word: WordCreate, unit_id: str):
    db_word = schema.Word(**word.dict(), vc_id=unit_id)
    db.add(db_word)
    db.commit()
    db.refresh(db_word)
    return db_word

def get_word(db: Session, word_id: str):
    return db.query(schema.Word).filter(schema.Word.vc_id == word_id).first()

def get_words(db: Session, skip: int = 0, limit: int = 10):
    return db.query(schema.Word).offset(skip).limit(limit).all()

def get_words_by_vocabulary(db: Session, vocabulary: List[str]):
    return db.query(schema.Word).filter(schema.Word.vc_vocabulary.in_(vocabulary)).all()

def get_words_by_ids(db: Session, ids: List[str]):
    return db.query(schema.Word).filter(schema.Word.vc_id.in_(ids)).all()

def get_words_in_batch(db: Session, batch_id: str):
    return db.query(schema.Word).join(schema.UserMemoryWord, schema.UserMemoryWord.word_id == schema.Word.vc_id).filter(schema.UserMemoryWord.batch_id == batch_id).all()

def update_word(db: Session, word_id: str, word: WordUpdate):
    db_word = db.query(schema.Word).filter(schema.Word.vc_id == word_id).first()
    if db_word:
        for key, value in word.dict(exclude_unset=True).items():
            setattr(db_word, key, value)
        db.commit()
        db.refresh(db_word)
        return db_word

def delete_word(db: Session, word_id: str):
    db_word = db.query(schema.Word).filter(schema.Word.vc_id == word_id).first()
    if db_word:
        db.delete(db_word)
        db.commit()
        return db_word
