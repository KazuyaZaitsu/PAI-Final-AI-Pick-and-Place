import argparse
import subprocess
import sys
from pathlib import Path

from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# PC部品の模擬検査データ
training_data = [
    ("起動正常 動作良好 異常なし 破損なし", "reuse"),
    ("電源が入る 動作確認済 破損なし", "reuse"),
    ("正常起動 検品合格 再利用可能", "reuse"),
    ("SSD正常 動作良好 検査合格", "reuse"),
    ("外観きれい 起動正常 故障なし", "reuse"),
    ("動作テスト合格 破損なし", "reuse"),
    ("電源が入らない 故障", "hold"),
    ("破損あり 部品が壊れている", "hold"),
    ("起動しない 異常あり", "hold"),
    ("動作不良 交換部品が必要", "hold"),
    ("SSD不良 検査不合格", "hold"),
    ("筐体が破損している 再利用不可", "hold"),
]

# AIモデルを学習
model = make_pipeline(
    TfidfVectorizer(analyzer="char", ngram_range=(2, 3)),
    MultinomialNB()
)

model.fit(
    [text for text, label in training_data],
    [label for text, label in training_data]
)

parser = argparse.ArgumentParser()
parser.add_argument("inspection", help="PC部品の検査結果")
parser.add_argument("--execute", action="store_true")
args = parser.parse_args()

# AIによる推論
result = model.predict([args.inspection])[0]

print("検査結果:", args.inspection, flush=True)
print(
    "AI判定:",
    "再利用可能" if result == "reuse" else "要確認",
    flush=True
)

if not args.execute:
    print("判定テストのみ。ロボットは動かしません。")

elif result == "reuse":
    print("ロボットアームによる搬送を開始します", flush=True)

    script = (
        Path(__file__).resolve().parent
        / "src/Pick-and-Place-Robotic-Arm-using-Ros2-"
        / "src/ur5e_gripper_gazebo/scripts"
        / "simple_pick_and_place.py"
    )

    subprocess.run([sys.executable, str(script)], check=True)

else:
    print("要確認のため自動搬送を停止します")
