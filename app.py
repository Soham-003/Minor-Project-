from flask import Flask, render_template, request
from src.pipeline.FP_predict_pipeline import PredictPipeline, CustomData
from src.pipeline.IR_predict_pipeline import IR_PredictPipeline, IR_CustomData
from src.logger import logging

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict-fertilizer', methods=['GET', 'POST'])
def predicting_fertilizer():
    try:
        if request.method == 'POST':
           
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

            
            return render_template('index.html', fertilizer=results)

    except Exception as e:
        logging.error(f"Error in prediction: {e}")
        return render_template('index.html', error="Something went wrong. Please try again.")

    
    return render_template('index.html')

@app.route('/irrigation-system', methods=['GET', 'POST'])
def predicting_irrigation():
    try:
        if request.method == 'POST':
           
            data =IR_CustomData(
                Soil_Moisture=float(request.form.get('Soil_Moisture')),
                Temperature=float(request.form.get('Temperature')),
                Soil_Humidity=float(request.form.get('Soil_Humidity')),
                Air_Humidity=float(request.form.get('Air_Humidity')),
                Pressure=float(request.form.get('Pressure')),
            )

            
            pred_df = data.get_data_as_dataframe()
            predict_pipeline = IR_PredictPipeline()
            results = predict_pipeline.predict(pred_df)
            logging.info(f"Prediction: {results}")

            if(results==0): results = "DO NOT IRRIGATE"
            else: results = "IRRIGATE"
            

            
            return render_template('index2.html', irrigation=results)

    except Exception as e:
        logging.error(f"Error in prediction: {e}")
        return render_template('index.html', error="Something went wrong. Please try again.")

    
    return render_template('index2.html')

if __name__ == "__main__":
    app.run(debug=True)
