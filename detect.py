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

def update_model(pattern: str, label: int):
    if os.path.exists('redos_model.pkl'):
        model = joblib.load('redos_model.pkl')
    else:
        model = SGDClassifier(loss="log_loss")
    X_new = [extract_features(pattern)]
    y_new = [label]
    model.partial_fit(X_new, y_new, classes=[0, 1])
    joblib.dump(model, 'redos_model.pkl')
    # git 자동 반영
    subprocess.run(["git", "add", "redos_model.pkl"])
    subprocess.run(["git", "commit", "-m", "Update model after detection learning"], check=False)
    subprocess.run(["git", "push"], check=False)

def predict_with_ai(pattern: str):
    features = extract_features(pattern)
    model = joblib.load('redos_model.pkl')
    proba = model.predict_proba([features])[0]
    pred = model.predict([features])[0]
    confidence = max(proba)
    if confidence < 0.7:  # 신뢰도 임계값(예: 70%) 미만이면 판단 불가
        return None
    return pred == 1

def main():
    regex = input("검사할 정규표현식을 입력하세요: ")
    result = predict_with_ai(regex)
    if result is None:
        print("🤔 AI가 확신을 갖고 분류하지 못했습니다. 직접 레이블을 입력해 주세요.")
        label_input = input("취약(1)/안전(0)/모름(Enter): ")
        if label_input in ["0", "1"]:
            label = int(label_input)
            update_model(regex, label)
        else:
            print("❗️레이블이 입력되지 않아 학습하지 않습니다.")
    elif result:
        print("⚠️ AI가 취약한 정규표현식으로 분류했습니다. ReDoS 위험이 있습니다.")
        update_model(regex, 1)
    else:
        print("✅ AI가 안전한 정규표현식으로 분류했습니다.")
        update_model(regex, 0)

if __name__ == "__main__":
<<<<<<< HEAD
    main()
=======
    main()
>>>>>>> 99faf56 (Update model after detection learning)
