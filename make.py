import sys
import joblib
from sklearn.linear_model import SGDClassifier
import os
import subprocess


input = sys.stdin.readline
def extract_features(pattern: str):
    return [
        len(pattern),
        pattern.count('('),
        pattern.count('+'),
        pattern.count('*'),
        pattern.count('?'),
        pattern.count('|'),
        pattern.count('{'),
        pattern.count('['),
    ]

# 기존 모델 불러오기 또는 새로 생성
if os.path.exists('redos_model.pkl'):
    model = joblib.load('redos_model.pkl')
else:
    model = SGDClassifier(loss="log_loss")

# filename = input("학습 데이터 파일명을 입력하세요 (예: regex_samples.txt): ").strip()
filename = input().strip()

patterns = []
labels = []

with open(filename, encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            pattern, label = line.rsplit(maxsplit=1)
            if label not in ["0", "1"]:
                continue
            patterns.append(pattern)
            labels.append(int(label))
        except ValueError:
            continue

if patterns:
    for p, l in zip(patterns, labels):
        X_new = [extract_features(p)]
        y_new = [l]
        model.partial_fit(X_new, y_new, classes=[0, 1])
    joblib.dump(model, 'redos_model.pkl')
    print(f"{len(patterns)}개의 데이터로 누적 학습 완료! (redos_model.pkl)")
    subprocess.run(["git", "add", "redos_model.pkl"])
    subprocess.run(["git", "commit", "-m", "Update model after batch training"], check=False)
    subprocess.run(["git", "push"], check=False)
else:
    print("입력된 데이터가 없습니다.")