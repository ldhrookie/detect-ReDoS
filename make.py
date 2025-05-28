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

print("시작")  # 실행 확인용

# 새로운 데이터 입력
new_pattern = input("새 정규표현식: ")
print("입력 완료")  # 입력 확인용
new_label = int(input("취약(1)/안전(0): "))

X_new = [extract_features(new_pattern)]
y_new = [new_label]

# 증분 학습
model.partial_fit(X_new, y_new, classes=[0, 1])

# 모델 저장
joblib.dump(model, 'redos_model.pkl')
print("모델이 성공적으로 학습되고 저장되었습니다! (redos_model.pkl)")

# git에 자동 반영
subprocess.run(["git", "add", "redos_model.pkl"])
subprocess.run(["git", "commit", "-m", "Update model after new training data"], check=False)
subprocess.run(["git", "push"], check=False)