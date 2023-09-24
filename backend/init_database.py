import pandas as pd
from database import SessionLocal, engine, Base
from database import operation as op
from database import schema
from memorize import *


Base.metadata.create_all(bind=engine)


def init():
    # init database
    book = pd.read_csv('DictionaryData/book.csv', sep=">")
    word = pd.read_csv('DictionaryData/word.csv', sep=">")
    relation_book_word = pd.read_csv('DictionaryData/relation_book_word.csv', sep=">")
    word_translation = pd.read_csv('DictionaryData/word_translation.csv')
    print(len(book), list(book.columns))
    print(len(word), list(word.columns))
    print(len(relation_book_word), list(relation_book_word.columns))
    print(len(word_translation), list(word_translation.columns))
    word_to_translation = {}
    for i in word_translation.iterrows():
        word_to_translation[i[1]['word']] = i[1]['translation']
    s = SessionLocal()
    book.fillna(value='', inplace=True)
    word.fillna(value='', inplace=True)
    relation_book_word.fillna(value='', inplace=True)
    for i in book.to_dict(orient='records'):
        i['bk_organization'] = i['bk_orgnization']
        del i['bk_orgnization']
        if i['bk_parent_id'] == '0':
            del i['bk_parent_id']
            i['bk_series_id'] = i['bk_id']
            del i['bk_id']
            s.add(schema.BookSeries(**i))
        else:
            del i['bk_parent_id']
            s.add(schema.Book(**i))
    s.commit()
    print("finish book")
    for i in word.to_dict(orient='records'):
        w = i['vc_vocabulary']
        if w in word_to_translation:
            i['vc_translation'] = word_to_translation[w]
        else:
            i['vc_translation'] = ''
        s.add(schema.Word(**i))
    s.commit()
    print("finish word")
    for i in relation_book_word.to_dict(orient='records'):
        s.add(schema.Unit(**i))
    s.commit()
    print("finish relation")

    email = "demo@demo.com"
    user = op.create_user(s, op.UserCreate(email=email, is_active=True))

    book_name = "雅思词汇词以类记"
    book_id = book[book['bk_name'] == book_name]['bk_id'].values[0]
    batch_size = 10
    userbook = op.create_user_book(s, op.UserBookCreate(owner_id=user.id, book_id=book_id, batch_size=batch_size, title=book_name, random=True))

if __name__ == "__main__":
    init()
