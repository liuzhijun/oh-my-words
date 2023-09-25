from sqlalchemy.orm import Session
from typing import List, Tuple
from database import schema
from database.operation import *
import random

# 记单词
from story_agent import generate_story_and_translated_story


def get_words_for_book(db: Session, user_book: UserBook) -> List[schema.Word]:
    book = get_book(db, user_book.book_id)
    if book is None:
        print("book not found")
        return []
    words = db.query(schema.Word).join(schema.Unit, schema.Unit.bv_voc_id == schema.Word.vc_id).filter(schema.Unit.bv_book_id == book.bk_id).all()
    return words

def track(db: Session, user_book: schema.UserBook, words: List[schema.Word]):
    batch_size = user_book.batch_size
    if user_book.random:
        random.shuffle(words)
    for i in range(0, len(words), batch_size):
        batch_words = words[i:i+batch_size]
        batch_words_str_list = [word.vc_vocabulary for word in batch_words]
        story, translated_story = generate_story_and_translated_story(batch_words_str_list)
        user_memory_batch = create_user_memory_batch(db, UserMemoryBatchCreate(
            user_book_id=user_book.id,
            story=story,
            translated_story=translated_story
        ))
        if i == 0:
            user_book.memorizing_batch = user_memory_batch.id
            db.commit()
        for word in batch_words:
            memory_word = UserMemoryWordCreate(
                batch_id=user_memory_batch.id,
                word_id=word.vc_id
            )
            db_memory_word = schema.UserMemoryWord(**memory_word.dict())
            db.add(db_memory_word)
        db.commit()

def remenber(db: Session, user_memory_word_id: str):
    return create_user_memory_action(db, UserMemoryActionCreate(
        user_memory_word_id=user_memory_word_id,
        action="remember"
    ))

def forget(db: Session, user_memory_word_id: str):
    return create_user_memory_action(db, UserMemoryActionCreate(
        user_memory_word_id=user_memory_word_id,
        action="forget"
    ))

def memory_batch_action(db: Session, actions: List[Tuple[str, str]]):
    """
    actions: [(user_memory_word_id, remember | forget)]
    """
    for user_memory_word_id, action in actions:
        memory_action = UserMemoryActionCreate(
            user_memory_word_id=user_memory_word_id,
            action=action
        )
        db_memory_action = schema.UserMemoryAction(**memory_action.dict())
        db.add(db_memory_action)
    db.commit()

def on_batch_start(db: Session, user_memory_batch_id: str):
    return create_user_memory_batch_action(db, UserMemoryBatchActionCreate(
        batch_id=user_memory_batch_id,
        action="start"
    ))

def on_batch_end(db: Session, user_memory_batch_id: str):
    return create_user_memory_batch_action(db, UserMemoryBatchActionCreate(
        batch_id=user_memory_batch_id,
        action="end"
    ))
