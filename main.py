from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.tokenfilter import CompoundNounFilter
import flet as ft
import time

# JanomeのTokenizerを初期化
tokenizer = Tokenizer()

# 文節ごとに分割するための設定
filters = [CompoundNounFilter()]  # 名詞の複合語を一つの単語にまとめるフィルター
analyzer = Analyzer(tokenizer=tokenizer, token_filters=filters)

def main(page: ft.Page):
    page.title = "Simple Rapid Reader JP"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    #変数
    global speed, reading, text
    speed = 120
    reading = False
    text = "Simple Rapid Reader JPへようこそ。ここに読みたい文章を入力してください。"

    # メインの処理
    def start_reading():
        global speed, reading
        reading = True
        words = word_split(text_box.value)
        for word in words:
            if not reading:
                break
            text_display.value = str(word)
            page.update()
            time.sleep(60 / speed)

    def word_split(text):
        # 文節ごとに分割
        chunks = []
        current_chunk = []

        tokens = list(analyzer.analyze(text))  # トークンをリストとして取得

        for i, token in enumerate(tokens):
            current_chunk.append(token.surface)

            # 次のトークンが存在する場合
            if i + 1 < len(tokens):
                next_token = tokens[i + 1]
                print("単語"+ token.surface)
                print(token.part_of_speech)
                # 助詞または助動詞であるかどうかをチェック
                if token.part_of_speech.startswith('助詞') or token.part_of_speech.startswith('助動詞') or token.part_of_speech.startswith('記号,空白') or token.part_of_speech.startswith('記号,読点') or token.part_of_speech.startswith('記号,句点'):
                        if not next_token.part_of_speech.startswith('助詞') and not next_token.part_of_speech.startswith('助動詞') and not next_token.part_of_speech.startswith('記号,読点') and not next_token.part_of_speech.startswith('記号,句点'):
                            chunks.append(''.join(current_chunk))
                            current_chunk = []
            else:
                # 最後のトークンの場合
                if token.part_of_speech.startswith('助詞') or token.part_of_speech.startswith('助動詞'):
                    chunks.append(''.join(current_chunk))
                else:
                    chunks.append(''.join(current_chunk))

        # スペースを削除
        chunks = [word for word in chunks if word != " "]  # スペースを削除
        return chunks

    # 速読を停止する関数
    def stop_reading():
        global reading
        reading = False

    # スピードを変更する関数
    def change_speed():
        global speed
        speed = speed_slider.value

    # ここから表示するUIの設定

    # テキストを表示するボックス
    text_display = ft.Text(
        value="hello",
        size=50,
        color="white",
        weight=ft.FontWeight.BOLD,
    )

    # 処理する文章を入力するテキストボックス
    text_box = ft.TextField(
        value=text,
        color="white",
        text_align=ft.TextAlign.LEFT,
        expand=True,
    )

    # スタートボタン。速読を開始するためのボタン。
    start_button = ft.ElevatedButton(
        text="Start",
        on_click=lambda _: start_reading()
    )

    # ストップボタン。速読を停止するためのボタン。
    stop_button = ft.ElevatedButton(
        text="Stop",
        on_click=lambda _: stop_reading()
    )

    # スピードを変更するスライダー
    speed_slider = ft.Slider(
        min=10,
        max=300,
        value=speed,
        on_change=lambda _: change_speed()
    )

    # UIの構築
    page.add(
        ft.Column(
            [
                ft.Row([text_display], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([start_button, stop_button], alignment=ft.MainAxisAlignment.CENTER),
                speed_slider,
                ft.Row([text_box], alignment=ft.MainAxisAlignment.CENTER)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        )
    )

ft.app(target=main)