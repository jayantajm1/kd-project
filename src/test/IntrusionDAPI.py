from flask import Flask, request, jsonify
import pickle
import numpy as np

# Load trained model
with open('D:\ked-ml-project\ked-ml-project\Final-Year-Project\models\keylogger_intrusion_model.pkl', 'rb') as file:
    model = pickle.load(file)

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON input (assumed to be a list of features)
        data = request.get_json()
        features = np.array(data['features']).reshape(1, -1)

        # Predict using the model
        prediction = model.predict(features)
        result = 'Malicious' if prediction[0] == 1 else 'Normal'

        return jsonify({'prediction': result})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
