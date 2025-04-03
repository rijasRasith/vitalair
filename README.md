#AQI-Prediction and HRI Prediction 

Welcome to the repository for the “Predicting the Air Quality Index of Indian Cities using Machine Learning”, where the goal is to forecast the Air Quality Index (AQI) for major Indian AQI stations for the upcoming 28 days using machine learning techniques(Nbeats and GPR). 

Air quality monitoring is crucial for our well-being, and this competition utilizes historical daily averages of various air pollutants to build accurate models that can predict the AQI for each station. Our team has extensively analyzed the data and constructed models that we believe will help us achieve our objective.

To navigate the repo:
- All the code for EDA and modeling can be found in the notebooks directory , the model.ipynb is the file that contains the codes we used for machine learning model.
- `each station training` directory contains 12 air qualtiy monitoring station's of tamilnadu  data used for training and the model. It also contains the next 28 days predicted results in  `forecasted results` directory.
- `combined_AQI_forecast.csv` contains the forecasted AQI results of all the 12 stations 
- Rest of the notebook contains code for H2O-wave app we built.
  - `app.py` is the main script to run the wave-app.
  - `components`, `pages`, and `utils` directory contain scripts in a modular fashion to support different tabs/sections in the app.
 

HRI prediction and potential health risks mapping for all those 12 stations is pending