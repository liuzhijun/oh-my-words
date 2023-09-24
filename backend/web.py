import gradio as gr
from database.operation import *
from memorize import *
from database import SessionLocal, engine, Base

import pandas as pd
from collections import defaultdict


Base.metadata.create_all(bind=engine)
db = SessionLocal()

users = get_all_users(db)
# book_series_list = get_book_series_list(db)
books = get_all_books(db)

# print(users, books)

with gr.Blocks() as demo:
    gr.Markdown("# 批量记单词")
    gr.Markdown(f"共 {len(books)} 本书")
    # with gr.Accordion("Open for More!"): # 折叠
    gr.Markdown("本项目基于[开源数据集](https://github.com/LinXueyuanStdio/DictionaryData)，并且[开源代码](https://github.com/LinXueyuanStdio/oh-my-words)，欢迎大家贡献代码～")

    # 1. 创建记忆计划
    with gr.Tab("创建记忆计划"):
        batch_size = gr.State(value=10)

        select_user = gr.Dropdown(
            [f"{user.email}  [{user.id}]" for user in users], label="用户", info=""
        )
        # select_book_series = gr.Dropdown(
        #     book_series_list, label="系列", info="选择一个系列"
        # )
        select_book = gr.Dropdown(
            [f"{book.bk_name}  [{book.bk_id}]" for book in books],
            # books,
            label="单词书", info="选择一本单词书"
        )
        # def on_select_user(user):
        #     select_user.
        #     return user
        # select_user.change(on_select_user, inputs=[], outputs=[])
        batch_size = gr.Number(value=10, label="批次大小")
        random = gr.Checkbox(value=True, label="以单词乱序进行记忆")
        title = gr.TextArea(value='单词书', lines=1)
        btn = gr.Button("创建记忆计划")
        status = gr.Textbox("", lines=1, label="状态")
        def submit(user, book, title, random, batch_size):
            user_id = user.split(" [")[1][:-1]
            book_id = book.split(" [")[1][:-1]
            user_book = create_user_book(db, UserBookCreate(
                owner_id=user_id,
                book_id=book_id,
                title=title,
                random=random,
                batch_size=batch_size
            ))
            if user_book is not None:
                return "成功"
            else:
                return "失败"

        btn.click(submit, [select_user, select_book, title, random, batch_size], [status])

    # 选择单词分批
    with gr.Tab("选择单词分批"):
        select_user = gr.Dropdown(
            [f"{user.email}  [{user.id}]" for user in users], label="用户", info=""
        )
        select_user_book = gr.Dropdown(
            [], label="记忆计划", info="请选择记忆计划"
        )
        word_count = gr.Number(value=0, label="单词个数")
        known_words = gr.CheckboxGroup(
            [], label="已学会的单词", info="正式记忆前将去除已学会的单词，提高每个批次的新词密度，进而提高效率"
        )
        btn = gr.Button("生成批次", elem_id="btn", elem_classes=["abc", "def"])
        status = gr.Textbox("", lines=1, label="生成结果")

        def on_select_user(user):
            print('user', user)
            if user is None:
                return gr.Dropdown.update(choices=[])
            new_options =  []
            user_id = user.split(" [")[1][:-1]
            user_book = get_user_books_by_owner_id(db, user_id)
            new_options = [f"{book.title} | {book.batch_size}个单词一组 [{book.id}]" for book in user_book]
            return gr.Dropdown.update(choices=new_options)

        def on_select_user_book(user_book):
            print('user_book', user_book)
            if user_book is None:
                return 0, gr.CheckboxGroup.update(choices=[])
            new_options = []
            user_book_id = user_book.split(" [")[1][:-1]
            user_book = get_user_book(db, user_book_id)
            book_id = user_book.book_id
            book = get_book(db, book_id)
            if book is None:
                return 0, gr.CheckboxGroup.update(choices=[])
            words = get_words_for_book(db, user_book)
            new_options = [f"{word.vc_vocabulary}" for word in words]
            return len(words), gr.CheckboxGroup.update(choices=new_options)

        select_user.select(on_select_user, inputs=[select_user], outputs=[select_user_book])
        select_user_book.select(on_select_user_book, inputs=[select_user_book], outputs=[word_count, known_words])

        def submit(user_book, known_words):
            user_book_id = user_book.split(" [")[1][:-1]
            user_book = get_user_book(db, user_book_id)
            all_words = get_words_for_book(db, user_book)
            unknown_words = []
            for w in all_words:
                if w.vc_vocabulary not in known_words:
                    unknown_words.append(w)
            track(db, user_book, unknown_words)
            return "成功"

        btn.click(submit, [select_user_book, known_words], [status])

    # 记忆
    with gr.Tab("记忆"):
        select_user = gr.Dropdown(
            [f"{user.email}  [{user.id}]" for user in users], label="用户", info=""
        )
        select_user_book = gr.Dropdown(
            [], label="记忆计划", info="请选择记忆计划"
        )
        memorizing_dataframe = gr.Dataframe(
            headers=["单词", "意思", "id", "记忆量"],
            datatype=["str", "str", "str", "str"],
            col_count=(4, "fixed"),
            wrap=True,
        )
        batches = gr.State(value=[])
        current_batch_index = gr.State(value=-1)
        with gr.Row():
            # story = gr.HighlightedText([])
            # translated_story = gr.HighlightedText([])
            # story = gr.Textbox()
            # translated_story = gr.Textbox()
            story = gr.Markdown()
            translated_story = gr.Markdown()
            # 试了一下，还是 markdown 的显示效果好

        memorize_action = gr.CheckboxGroup(choices=[], label="记住的单词", info="能够复述出意思才算记住")
        with gr.Row():
            previous_batch_btn = gr.Button("上一批")
            next_batch_btn = gr.Button("下一批", variant="primary")
        progress = gr.Slider(1, 1, value=1, step=1, label="进度", info="")

        def on_select_user(user):
            # print('user', user)
            if user is None:
                return gr.Dropdown.update(choices=[])
            new_options =  []
            user_id = user.split(" [")[1][:-1]
            user_book = get_user_books_by_owner_id(db, user_id)
            new_options = [f"{book.title} | {book.batch_size}个单词一组 [{book.id}]" for book in user_book]
            return gr.Dropdown.update(choices=new_options)

        def process(story: str):
            # return [(i, "") for i in story.split(" ")]
            return story.replace("[", "**").replace("]", "**")
        def update_batch(memorizing_batch: UserMemoryBatch):
            new_options = []
            word_df = []
            # print(get_user_memory_batch(db, memorizing_batch.id))
            # print(memorizing_batch.id)
            # print(get_user_memory_words_by_batch_id(db, memorizing_batch.id))
            # print(get_words_by_ids(db, [w.word_id for w in get_user_memory_words_by_batch_id(db, memorizing_batch.id)]))
            # words = get_words_in_batch(db, memorizing_batch.id)
            # words = get_words_by_ids(db, [w.word_id for w in memorizing_words])
            memorizing_words = get_user_memory_words_by_batch_id(db, memorizing_batch.id)
            word_to_memorizing = {mw.word_id:mw.id for mw in memorizing_words}
            memorizing_to_word = {mw.id:mw.word_id for mw in memorizing_words}
            words = get_words_by_ids(db, [w.word_id for w in memorizing_words])
            actions = get_actions_at_each_word(db, [w.id for w in memorizing_words])
            remember_count = defaultdict(int)
            forget_count = defaultdict(int)
            for a in actions:
                if a.action == "remember":
                    remember_count[memorizing_to_word[a.user_memory_word_id]] += 1
                else:
                    forget_count[memorizing_to_word[a.user_memory_word_id]] += 1
            for w in words:
                new_options.append(f"{w.vc_vocabulary}")
                word_df.append([w.vc_vocabulary, w.vc_translation, word_to_memorizing[w.vc_id], f"{remember_count[w.vc_id]} / {remember_count[w.vc_id] + forget_count[w.vc_id]}"])
            df = pd.DataFrame(word_df, columns=["单词", "意思", "id", "记忆量"])
            # print(df)
            # print(new_options)
            story = memorizing_batch.story
            story = process(story)
            # print(story)
            translated_story = memorizing_batch.translated_story
            translated_story = process(translated_story)
            # print(translated_story)
            # df = gr.DataFrame.update(
            #     value=df,
            #     max_rows=len(df),
            # )
            return (df, story, translated_story, gr.CheckboxGroup.update(choices=new_options))

        def on_select_user_book(user_book: str):
            """
            1. 当前单词
            2. 对当前单词的操作
            3. 故事
            """
            # print('user_book', user_book)
            if user_book is None:
                # 为什么会空？这里返回的东西可能会爆炸，但好像执行不到这里
                # 不管了，放个告示牌在这里，大家看见这个坑请绕着走
                return [], gr.CheckboxGroup.update(choices=[])
            user_book_id: str = user_book.split(" [")[1][:-1]
            user_book = get_user_book(db, user_book_id)
            batches = get_user_memory_batches_by_user_book_id(db, user_book_id)
            batch_id = user_book.memorizing_batch
            memorizing_batch = get_user_memory_batch(db, batch_id)
            current_batch_index = -1
            if memorizing_batch is not None:
                for index, b in enumerate(batches):
                    if b.id == memorizing_batch.id:
                        current_batch_index = index
                        break
            if current_batch_index == -1:
                current_batch_index = 0
                memorizing_batch = batches[0]
                batch_id = memorizing_batch.id
                user_book.memorizing_batch = batch_id
                update_user_book(db, user_book_id, UserBookUpdate(
                    owner_id=user_book.owner_id,
                    book_id=user_book.book_id,
                    title=user_book.title,
                    batch_size=user_book.batch_size,
                    memorizing_batch=batch_id
                ))
            updates = update_batch(memorizing_batch)
            # print(len(batches))
            return (batches, current_batch_index) + updates + (
                    gr.Slider.update(
                        minimum=1,
                        maximum=len(batches),
                        value=current_batch_index,
                    ),)

        batch_widget = [memorizing_dataframe, story, translated_story, memorize_action]
        select_user.select(on_select_user, inputs=[select_user], outputs=[select_user_book])
        select_user_book.select(
            on_select_user_book,
            inputs=[select_user_book],
            outputs=[batches, current_batch_index] + batch_widget + [progress]
        )

        def submit_batch(batches, current_batch_index):
            memorizing_batch = batches[current_batch_index]
            updates = update_batch(memorizing_batch)
            return updates + (gr.Slider.update(value=current_batch_index+1),)
        def previous_batch(batches, current_batch_index):
            if current_batch_index <= 0:
                current_batch_index = 0
            elif current_batch_index > 0:
                current_batch_index -= 1
            return submit_batch(batches, current_batch_index)
        def next_batch(batches: List[UserMemoryBatch], current_batch_index: int, memorizing_dataframe: pd.DataFrame, memorize_action: List[str]):
            old_index = current_batch_index
            if current_batch_index >= len(batches)-1:
                current_batch_index = len(batches)-1
            elif current_batch_index < len(batches) - 1:
                current_batch_index += 1
            if current_batch_index != old_index:
                # 下一页之前需要保存记忆进度
                # print("下一页之前需要保存记忆进度")
                # print(memorizing_dataframe)
                # print(memorize_action)
                old_batch = batches[old_index]
                actions = []
                for i in range(len(memorizing_dataframe)):
                    row = memorizing_dataframe.iloc[i]
                    word_i = row["单词"]
                    memorizing_i = row["id"]
                    if word_i in memorize_action:
                        actions.append((memorizing_i, "remember"))
                    else:
                        actions.append((memorizing_i, "forget"))
                memory_batch_action(db, actions)
            return submit_batch(batches, current_batch_index)
        previous_batch_btn.click(
            previous_batch,
            inputs=[batches, current_batch_index],
            outputs=batch_widget + [progress]
        )
        next_batch_btn.click(
            next_batch,
            inputs=[batches, current_batch_index, memorizing_dataframe, memorize_action],
            outputs=batch_widget + [progress]
        )

demo.launch()
