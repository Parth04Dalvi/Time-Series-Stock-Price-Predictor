📈 Time-Series Stock Price Predictor
A Data Science Simulation for Financial Forecasting
This project is a single-page web application that simulates an end-to-end stock price prediction service. It demonstrates a robust architecture for time-series analysis, integrating a mock Python machine learning backend with a modern, highly responsive financial dashboard.

The application allows users to input a stock ticker and a prediction horizon, visualizing the historical data alongside the future forecast and its associated uncertainty.

✨ Key Technical Skills Demonstrated
This project is an excellent showcase of multi-disciplinary technical abilities:

Skill Area

Features Demonstrated

Data Science / ML

Simulation of an ARIMA/RNN model for time-series forecasting in the Python backend.

Prediction Modeling

Calculation and visualization of Prediction Confidence Intervals (CI), showcasing an understanding of model uncertainty and statistical accuracy.

Full-Stack Architecture

Clear separation between the simulated Python backend (data processing) and the HTML/JS frontend (data visualization).

Advanced Visualization

Utilization of Chart.js to display complex datasets, including plotting the historical and predicted line, and rendering the CI band as a shaded area.

Fintech UI/UX

Professional, data-driven dashboard design featuring a dark control panel, clear Key Performance Indicators (KPIs), and dynamic icons for immediate visual feedback.

🛠️ Technology Stack
Frontend: HTML5, Tailwind CSS (for modern, responsive styling)

Visualization: Chart.js v4+ (for dynamic, interactive stock charts and CI bands)

Core Logic: Vanilla JavaScript (simulating asynchronous API calls)

Backend Simulation: Python (conceptual code demonstrating ML pipeline steps)

🚀 How to Use the Simulator
The entire application runs from the single index.html file, which includes all the mock data generation logic necessary to function without a real API key or live Python server.

Open the file: Load stock_predictor/index.html in any modern web browser.

Input Data: Enter a stock ticker (e.g., GOOG, AAPL) and the number of days you wish to predict (1-30).

Run Model: Click the "Run Prediction Model" button. The UI will display a loading spinner to simulate the model training time.

Analyze Results:

KPIs: Review the latest price and the Projected Price Change (with dynamic up/down arrows).

Chart: The main visualization displays the Historical Price (solid green line) and the Predicted Price (dashed indigo line).

Uncertainty: The shaded blue band around the predicted line represents the 95% Confidence Interval, demonstrating how prediction certainty decreases the further you look into the future.
