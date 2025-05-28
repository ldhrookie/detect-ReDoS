import joblib
from sklearn.linear_model import SGDClassifier
import os
import subprocess

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

print("정규표현식과 레이블(취약:1, 안전:0)을 한 줄에 입력하세요. (예: (a+)+ 1)")
print("입력을 마치려면 빈 줄(Enter)만 입력하세요.")

patterns = []
labels = []

while True:
    line = input("입력: ")
    if not line.strip():
        break
    try:
        pattern, label = line.rsplit(maxsplit=1)
        if label not in ["0", "1"]:
            print("레이블은 0 또는 1만 입력하세요.")
            continue
        patterns.append(pattern)
        labels.append(int(label))
    except ValueError:
        print("형식: 정규표현식 0 또는 정규표현식 1 (예: (a+)+ 1)")
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