import pickle

model, vectorizer = pickle.load(open("model/model.pkl", "rb"))

def predict_category(goal):
    goal_vec = vectorizer.transform([goal])
    return model.predict(goal_vec)[0]