from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.tokenfilter import CompoundNounFilter

# JanomeのTokenizerを初期化
tokenizer = Tokenizer()

# 文節ごとに分割するための設定
filters = [CompoundNounFilter()]  # 名詞の複合語を一つの単語にまとめるフィルター
analyzer = Analyzer(tokenizer=tokenizer, token_filters=filters)

# サンプルテキスト
text = "私は学校に行きます。今日は天気が良いです。Today is a good day."

# 文節ごとに分割
chunks = []
current_chunk = []

tokens = list(analyzer.analyze(text))  # トークンをリストとして取得

for i, token in enumerate(tokens):
    current_chunk.append(token.surface)

    # 次のトークンが存在する場合
    if i + 1 < len(tokens):
        next_token = tokens[i + 1]
        # 助詞または助動詞であるかどうかをチェック
        if token.part_of_speech.startswith('助詞') or token.part_of_speech.startswith('助動詞') or token.part_of_speech.startswith('記号'):
            if not next_token.part_of_speech.startswith('記号'):
                chunks.append(''.join(current_chunk))
                current_chunk = []
    else:
        # 最後のトークンの場合
        if token.part_of_speech.startswith('助詞') or token.part_of_speech.startswith('助動詞'):
            chunks.append(''.join(current_chunk))
        else:
            chunks.append(''.join(current_chunk))

# 結果を表示
for chunk in chunks:
    print(chunk)