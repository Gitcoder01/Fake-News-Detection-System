from explain import explain_prediction

text = """
Scientists discovered a miracle drug that instantly cures every disease.
"""

result = explain_prediction(text)

for word, weight in result:
    print(f"{word}: {weight:.4f}")