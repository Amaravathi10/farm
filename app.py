from flask import Flask, request, render_template
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import NearestNeighbors
import pickle
from googletrans import Translator, constants

app = Flask(__name__)
translator = Translator(service_urls=['translate.google.com'])

def t(text):
    """Translate English text to Telugu."""
    try:
        translation = translator.translate(text, dest='te')
        return translation.text
    except Exception as e:
        print(f"Translation error: {e}")
        return text

# Load the saved model and averages
with open('rf_model.pkl', 'rb') as model_file:
    rf_model = pickle.load(model_file)

with open('averages.pkl', 'rb') as avg_file:
    averages = pickle.load(avg_file)

avg_temp, avg_humidity, avg_ph, avg_rainfall = averages['temp'], averages['humidity'], averages['ph'], averages['rainfall']

def predict_crop(N, P, K):
    input_data = np.array([[N, P, K, avg_temp, avg_humidity, avg_ph, avg_rainfall]])
    prediction = rf_model.predict(input_data)
    return prediction[0]

def find_similar_crops(N, P, K, main_recommendation, n_neighbors=6):
    df = pd.read_csv('Crop_recommendation.csv')
    crop_avg = df.groupby('label')[['N', 'P', 'K']].mean().reset_index()

    nbrs = NearestNeighbors(n_neighbors=n_neighbors, metric='euclidean')
    nbrs.fit(crop_avg[['N', 'P', 'K']])

    distances, indices = nbrs.kneighbors([[N, P, K]])

    similar_crops = []
    for idx, distance in zip(indices[0], distances[0]):
        crop_data = crop_avg.iloc[idx]
        if crop_data['label'] != main_recommendation:
            adjustment = {
                'crop': crop_data['label'],
                'target_N': crop_data['N'],
                'target_P': crop_data['P'],
                'target_K': crop_data['K'],
                'N_diff': crop_data['N'] - N,
                'P_diff': crop_data['P'] - P,
                'K_diff': crop_data['K'] - K,
                'distance': distance
            }
            similar_crops.append(adjustment)

    return similar_crops[:5]

def print_adjustment(current_value, target_value, nutrient):
    diff = target_value - current_value
    if diff > 0:
        return f"{t('increase by')} {abs(diff):.2f} {t('to reach target')} {nutrient} {t('of')} {target_value:.2f}"
    elif diff < 0:
        return f"{t('decrease by')} {abs(diff):.2f} {t('to reach target')} {nutrient} {t('of')} {target_value:.2f}"
    else:
        return f"{t('no change needed')} ({t('current and target')} {nutrient}: {current_value:.2f})"

# Add the t function to Jinja2 environment
@app.context_processor
def inject_t():
    return dict(t=t)

@app.route('/')
def home():
    return render_template('index.html', title=t("Crop Recommendation System"))

@app.route('/predict', methods=['POST'])
def predict():
    try:
        N = float(request.form['N'])
        P = float(request.form['P'])
        K = float(request.form['K'])

        recommended_crop = predict_crop(N, P, K)
        result = {
            'recommended_crop': t(f"Best recommended crop: {recommended_crop}"),
            'similar_crops': []
        }

        similar_crops = find_similar_crops(N, P, K, recommended_crop)
        if similar_crops:
            result['similar_crops'].append(t("Alternative crops you could grow with NPK adjustments:"))
            result['similar_crops'].append(t(f"Your current NPK values - N: {N:.2f}, P: {P:.2f}, K: {K:.2f}"))

            for crop in similar_crops:
                crop_info = f"\n{t('Crop')}: {crop['crop']}\n{t('Required NPK adjustments')}:"
                crop_info += f"\n{t('N')}: {print_adjustment(N, crop['target_N'], 'N')}"
                crop_info += f"\n{t('P')}: {print_adjustment(P, crop['target_P'], 'P')}"
                crop_info += f"\n{t('K')}: {print_adjustment(K, crop['target_K'], 'K')}"
                result['similar_crops'].append(crop_info)

        return jsonify({'success': True, 'result': result})

    except Exception as e:
        return jsonify({'success': False, 'error': t("Error processing your request. Please enter valid numerical values.")})

if __name__ == '__main__':
    app.run(debug=True)