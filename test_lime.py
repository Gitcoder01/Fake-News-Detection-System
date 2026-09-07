from explain import explain_prediction

text = """
Scientists discovered a miracle drug that instantly cures every disease.
"""

result = explain_prediction(text)

for item in result:
    print(f"{item['word']}: {item['weight']:.4f}")