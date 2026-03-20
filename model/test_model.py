import pickle

# load model
model, vectorizer = pickle.load(open("model/model.pkl", "rb"))

# test input
goal = input("Enter goal: ")

# transform
goal_vec = vectorizer.transform([goal])

# predict
prediction = model.predict(goal_vec)

print("Predicted Category:", prediction[0])