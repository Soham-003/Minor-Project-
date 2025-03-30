from flask import Flask, render_template, request
from src.pipeline.FP_predict_pipeline import PredictPipeline, CustomData
from src.logger import logging

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def predicting_fertilizer():
    try:
        if request.method == 'POST':
            # Extract form data
            data = CustomData(
                N=float(request.form.get('nitrogen')),
                P=float(request.form.get('phosphorous')),
                K=float(request.form.get('potassium')),
                temperature=float(request.form.get('temperature')),
                humidity=float(request.form.get('humidity')),
                moisture=float(request.form.get('moisture')),
                soil_type=request.form.get('soil_type'),
                crop=request.form.get('crop_type')
            )

            # Convert data to DataFrame and predict
            pred_df = data.get_data_as_dataframe()
            predict_pipeline = PredictPipeline()
            results = predict_pipeline.predict(pred_df)
            logging.info(f"Prediction: {results}")

            if(results==0): results = "10-26-26"
            elif(results==1): results = "28-28"
            elif(results==2): results = "14-35-14"
            elif(results==3): results = "DAP"
            elif(results==4): results = "17-17-17"
            elif(results==5): results = "20-20"
            else: results = "Urea"

            # Return the index.html with fertilizer prediction
            return render_template('index.html', fertilizer=results)

    except Exception as e:
        logging.error(f"Error in prediction: {e}")
        return render_template('index.html', error="Something went wrong. Please try again.")

    # Ensure we always return a response
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
