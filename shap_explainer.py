import shap
import pickle

model = pickle.load(open("model.pkl", "rb"))

explainer = shap.TreeExplainer(model)

def get_shap_values(input_data):
    return explainer.shap_values(input_data)