# oh-my-words
记单词捏

目标场景：只考虑记住单词及其意思，使得能无障碍阅读，不考虑用于写作。

主要想法：批次记单词，每批 n 个单词，这 n 个单词用 AI 生成故事，复述故事即可记住单词。

为什么？

- [x] 批次记单词，一次可以记住 n 个单词，而不是一个一个记，效率高。
- [x] 复述故事，即费曼学习法，故事是单词的记忆之锚。
- [x] 复述故事而不是复述单词，故事具有连续性，更符合人类天性，容易记。

# 使用

1. 下载数据（[单词书数据源](https://github.com/LinXueyuanStdio/DictionaryData)）
    ```bash
    git clone https://github.com/LinXueyuanStdio/DictionaryData.git
    cd DictionaryData
    unzip relation_book_word.zip
    cd ..
    ```
2. 安装依赖
    ```bash
    pip install -r requirements.txt
    ```
3. 初始化数据库
    ```bash
    python init_database.py
    ```
4. 启动！
    ```bash
    python web.py
    ```
