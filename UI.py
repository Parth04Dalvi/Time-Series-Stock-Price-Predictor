<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Time-Series Stock Price Predictor</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.2/dist/chart.umd.min.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap');
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f4f7f9;
        }
        .card {
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
        }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #10b981; /* Emerald-500 */
            border-radius: 50%;
            width: 24px;
            height: 24px;
            animation: spin 1s linear infinite;
        }
        /* Specific spinner color for dark panel contrast */
        .dark-spinner {
            border-top: 4px solid #ffffff;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>

    <div id="app" class="min-h-screen p-4 md:p-8">
        <!-- Header -->
        <header class="mb-8 border-b pb-4">
            <h1 class="text-4xl font-extrabold text-gray-900 flex items-center">
                <svg class="w-8 h-8 mr-3 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 12l3-3 3 3 4-4M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-5 4v-4m0 0l-3 3m3-3l3 3"></path></svg>
                Time-Series Stock Price Predictor
            </h1>
            <p class="text-gray-500 mt-1">Simulating a Data Science backend for financial forecasting.</p>
        </header>

        <!-- Input and Configuration (Dark Control Panel Redesign) -->
        <div class="card bg-gray-800 p-6 rounded-xl mb-8 grid grid-cols-1 md:grid-cols-4 gap-4 items-end text-white shadow-xl">
            <div>
                <label for="ticker" class="block text-sm font-medium text-gray-300">Stock Ticker (e.g., GOOG, AAPL)</label>
                <input type="text" id="ticker" value="GOOG" class="mt-1 block w-full p-2 border border-gray-600 rounded-lg uppercase shadow-sm focus:ring-emerald-500 focus:border-emerald-500 bg-gray-700 text-white">
            </div>
            <div>
                <label for="prediction-days" class="block text-sm font-medium text-gray-300">Prediction Days (Max 30)</label>
                <input type="number" id="prediction-days" value="14" min="1" max="30" class="mt-1 block w-full p-2 border border-gray-600 rounded-lg shadow-sm focus:ring-emerald-500 focus:border-emerald-500 bg-gray-700 text-white">
            </div>
            <div class="md:col-span-2">
                <button onclick="runPrediction()" id="run-button" class="w-full py-2.5 px-4 bg-emerald-500 text-white font-bold rounded-lg hover:bg-emerald-400 transition duration-200 shadow-xl flex items-center justify-center">
                    <span id="button-text">Run Prediction Model</span>
                    <div id="loading-spinner" class="spinner dark-spinner hidden ml-3"></div>
                </button>
            </div>
        </div>

        <!-- Metrics and Chart Display -->
        <div id="results-area" class="space-y-6 hidden">
            
            <!-- Key Performance Indicators (KPIs) - Redesigned Cards with Icons -->
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-6">
                
                <!-- KPI 1: Latest Known Price -->
                <div class="card bg-white p-6 rounded-xl border-t-8 border-emerald-500 flex items-center space-x-4">
                    <svg class="w-8 h-8 text-emerald-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8V9m0 3v1m0 3v1"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    <div>
                        <p class="text-sm font-medium text-gray-500">Latest Known Price</p>
                        <p id="kpi-latest-price" class="text-2xl md:text-3xl font-bold text-gray-900 mt-1">--</p>
                    </div>
                </div>

                <!-- KPI 2: Projected Price Change (Dynamic Icon and Color) -->
                <div class="card bg-white p-6 rounded-xl border-t-8 border-indigo-500 flex items-center space-x-4">
                    <div id="kpi-change-icon" class="w-8 h-8 flex-shrink-0">
                        <!-- Icon injected by JS based on positive/negative change -->
                    </div>
                    <div>
                        <p class="text-sm font-medium text-gray-500">Projected Price Change</p>
                        <p id="kpi-change" class="text-2xl md:text-3xl font-bold text-gray-900 mt-1">--</p>
                    </div>
                </div>

                <!-- KPI 3: Predicted Price (End Date) -->
                <div class="card bg-white p-6 rounded-xl border-t-8 border-red-500 flex items-center space-x-4">
                    <svg class="w-8 h-8 text-red-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0l-3-3m3 3l3-3m-6 0h6m-3-3V5a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2z"></path></svg>
                    <div>
                        <p class="text-sm font-medium text-gray-500">Predicted Price (End Date)</p>
                        <p id="kpi-predicted-end" class="text-2xl md:text-3xl font-bold text-gray-900 mt-1">--</p>
                    </div>
                </div>
            </div>

            <!-- Prediction Chart -->
            <div class="card bg-white p-6 rounded-xl">
                <h2 class="text-xl font-semibold mb-4 text-gray-800" id="chart-title">Price Trend and Forecast for GOOG</h2>
                <div class="h-96">
                    <canvas id="priceChart"></canvas>
                </div>
            </div>
        </div>

        <!-- Initial Placeholder Message -->
        <div id="initial-message" class="text-center p-12 bg-white rounded-xl shadow-lg">
            <svg class="w-16 h-16 mx-auto text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 19V6l12-3v13.75M9 19c0 1.657-1.79 3-4 3s-4-1.343-4-3 1.79-3 4-3 4 1.343 4 3zM12 4s2-2 4-2 4 2 4 2v10c-2 0-4 2-4 2s-4-2-4-2V4zM12 4v16M21 3v15.75c0 1.657-1.79 3-4 3s-4-1.343-4-3 1.79-3 4-3z"></path></svg>
            <h3 class="mt-4 text-lg font-medium text-gray-900">Start Your Forecast</h3>
            <p class="mt-1 text-sm text-gray-500">Enter a stock ticker and the number of days you wish to predict, then click "Run Prediction Model" to see the forecast.</p>
        </div>
        
    </div>

    <script>
        // --- Global Variables ---
        let priceChartInstance = null;

        // --- Utility Functions ---

        function formatCurrency(value) {
            return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(value);
        }

        function formatPercentage(latest, predicted) {
            const change = predicted - latest;
            const percentage = (change / latest) * 100;
            const sign = percentage >= 0 ? '+' : '';
            return `<span class="${change >= 0 ? 'text-green-600' : 'text-red-600'} font-bold">${sign}${percentage.toFixed(2)}%</span>`;
        }

        // --- NEW UTILITY FUNCTION: Generates SVG icon based on change direction ---
        function getChangeIcon(change) {
            const isPositive = change >= 0;
            const color = isPositive ? 'text-green-500' : 'text-red-500';
            const iconPath = isPositive 
                ? 'M5 10l7-7m0 0l7 7m-7-7v18' // Up arrow
                : 'M19 14l-7 7m0 0l-7-7m7 7V3'; // Down arrow
            
            return `<svg class="w-8 h-8 ${color} flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="${iconPath}"></path></svg>`;
        }
        // --------------------------------------------------------------------------

        function setLoadingState(isLoading) {
            const runButton = document.getElementById('run-button');
            const buttonText = document.getElementById('button-text');
            const spinner = document.getElementById('loading-spinner');

            if (isLoading) {
                runButton.disabled = true;
                buttonText.textContent = 'Modeling...';
                spinner.classList.remove('hidden');
            } else {
                runButton.disabled = false;
                buttonText.textContent = 'Run Prediction Model';
                spinner.classList.add('hidden');
            }
        }

        // --- Core Prediction Logic (Simulates Python Backend Call) ---

        /**
         * Simulates the API call to the Python model.
         */
        function simulate_api_call(ticker, predictionDays) {
            return new Promise(resolve => {
                // Introduce artificial delay to mimic network latency and model training time
                setTimeout(() => {
                    const days = 90; // Historical days
                    const historicalData = [];
                    let basePrice = 150.00;
                    if (ticker === 'AAPL') basePrice = 180.00;
                    if (ticker === 'TSLA') basePrice = 250.00;
                    if (ticker === 'GOOG') basePrice = 145.00; // Adjusted for GOOG mock

                    let date = new Date();
                    date.setDate(date.getDate() - days);

                    // Generate Historical Data
                    for (let i = 0; i < days; i++) {
                        let price = basePrice + (i * 0.15) + (Math.random() - 0.5) * 2.0;
                        historicalData.push({
                            "date": date.toISOString().split('T')[0],
                            "price": Math.round(price * 100) / 100
                        });
                        date.setDate(date.getDate() + 1);
                    }
                    
                    // Generate Predicted Data
                    const predictedPrices = [];
                    let currentPrice = historicalData[historicalData.length - 1]['price'];

                    for (let i = 1; i <= predictionDays; i++) {
                        let trend = (Math.random() * 0.5) + 0.1; 
                        let noise = (Math.random() - 0.5) * 1.5;
                        
                        currentPrice = currentPrice * (1 + (trend + noise) / 100);
                        if (currentPrice < 50) currentPrice = 50;
                        
                        // Confidence Interval Logic
                        const confidence_multiplier = 0.005 + (i * 0.001); 
                        const lower_bound = currentPrice * (1 - confidence_multiplier);
                        const upper_bound = currentPrice * (1 + confidence_multiplier);

                        let futureDate = new Date();
                        futureDate.setDate(futureDate.getDate() + i);
                        
                        predictedPrices.push({
                            "date": futureDate.toISOString().split('T')[0],
                            "price": Math.round(currentPrice * 100) / 100,
                            "lower_bound": Math.round(lower_bound * 100) / 100,
                            "upper_bound": Math.round(upper_bound * 100) / 100
                        });
                    }

                    const latestPrice = historicalData[historicalData.length - 1]['price'];
                    
                    resolve({
                        ticker: ticker,
                        latest_price: latestPrice,
                        historical_data: historicalData,
                        predicted_data: predictedPrices
                    });
                }, 2500); // 2.5 seconds delay
            });
        }

        /** Main function to orchestrate the prediction and UI update. */
        async function runPrediction() {
            const ticker = document.getElementById('ticker').value.trim().toUpperCase();
            const days = parseInt(document.getElementById('prediction-days').value);
            
            if (!ticker || days < 1 || days > 30) {
                // Use the UI element to display error
                document.getElementById('initial-message').innerHTML = `
                    <p class="text-red-500 font-semibold">⚠️ Please enter a valid Ticker and Prediction Days (1-30).</p>
                `;
                document.getElementById('initial-message').classList.remove('hidden');
                document.getElementById('results-area').classList.add('hidden');
                return;
            }

            setLoadingState(true);
            document.getElementById('initial-message').classList.add('hidden');
            document.getElementById('results-area').classList.add('hidden');

            try {
                // Call the mock backend
                const result = await simulate_api_call(ticker, days);

                // Update KPIs
                const latestPrice = result.latest_price;
                const predictedPrice = result.predicted_data[result.predicted_data.length - 1].price;
                const change = predictedPrice - latestPrice; // Calculate change here

                document.getElementById('kpi-latest-price').textContent = formatCurrency(latestPrice);
                document.getElementById('kpi-predicted-end').textContent = formatCurrency(predictedPrice);
                
                // --- KPI Change update using new icon/color logic ---
                document.getElementById('kpi-change').innerHTML = formatPercentage(latestPrice, predictedPrice);
                document.getElementById('kpi-change-icon').innerHTML = getChangeIcon(change); 
                // --------------------------------------------------

                // Update Chart
                renderPriceChart(result);
                document.getElementById('chart-title').textContent = `Price Trend and Forecast for ${ticker}`;
                document.getElementById('results-area').classList.remove('hidden');

            } catch (error) {
                document.getElementById('initial-message').innerHTML = `
                    <p class="text-red-500 font-semibold">❌ Prediction Failed: ${error.message}</p>
                `;
                document.getElementById('initial-message').classList.remove('hidden');
                console.error("Prediction Error:", error);
            } finally {
                setLoadingState(false);
            }
        }


        // --- Chart Rendering ---

        function renderPriceChart(data) {
            if (priceChartInstance) priceChartInstance.destroy();

            const ctx = document.getElementById('priceChart').getContext('2d');

            // 1. Combine all data points for the X-Axis labels
            const allPoints = [...data.historical_data, ...data.predicted_data];
            const labels = allPoints.map(p => p.date);

            // 2. Prepare datasets
            const historicalPrices = data.historical_data.map(p => p.price);
            const predictedPrices = Array(data.historical_data.length).fill(NaN).concat(data.predicted_data.map(p => p.price));
            
            // Confidence Band Data
            const lowerBound = Array(data.historical_data.length).fill(NaN).concat(data.predicted_data.map(p => p.lower_bound));
            const upperBound = Array(data.historical_data.length).fill(NaN).concat(data.predicted_data.map(p => p.upper_bound));

            // Create a gradient fill for the historical data (looks professional)
            const historicalGradient = ctx.createLinearGradient(0, 0, 0, 400);
            historicalGradient.addColorStop(0, 'rgba(16, 185, 129, 0.4)'); // Emerald-500
            historicalGradient.addColorStop(1, 'rgba(16, 185, 129, 0.05)');

            priceChartInstance = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'Historical Price',
                            data: historicalPrices,
                            borderColor: '#10b981', // Emerald-500
                            backgroundColor: historicalGradient,
                            fill: true,
                            tension: 0.3,
                            pointRadius: 1,
                            borderWidth: 2,
                            order: 3 // Draw on top of history band
                        },
                        {
                            label: 'Predicted Price',
                            data: predictedPrices,
                            borderColor: '#6366f1', // Indigo-500
                            borderDash: [5, 5],
                            tension: 0.3,
                            fill: false,
                            pointRadius: 3,
                            pointBackgroundColor: '#6366f1',
                            borderWidth: 2,
                            order: 2 // Draw above the band
                        },
                        // Upper Bound (Line for band top)
                        {
                            label: 'Upper Bound (95% CI)',
                            data: upperBound,
                            borderColor: 'rgba(99, 102, 241, 0.2)', // Light Indigo
                            borderWidth: 1,
                            tension: 0.3,
                            pointRadius: 0,
                            fill: {
                                target: '+1', // Fill the area down to the next dataset (Lower Bound)
                                above: 'rgba(99, 102, 241, 0.1)', // Light fill color
                                below: 'rgba(99, 102, 241, 0.1)', 
                            },
                            order: 1 // Draw first (in the back)
                        },
                        // Lower Bound (Line for band bottom)
                        {
                            label: 'Lower Bound (95% CI)',
                            data: lowerBound,
                            borderColor: 'rgba(99, 102, 241, 0.2)', // Light Indigo
                            borderWidth: 1,
                            tension: 0.3,
                            pointRadius: 0,
                            fill: false,
                            order: 1 // Draw first (in the back)
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { 
                        legend: { 
                            position: 'top',
                            labels: {
                                // Hide the Upper/Lower bound lines in the legend, as they define the band
                                filter: (legendItem, chartData) => {
                                    return legendItem.datasetIndex !== 2 && legendItem.datasetIndex !== 3;
                                }
                            }
                        } 
                    },
                    scales: {
                        y: {
                            beginAtZero: false,
                            grid: { color: '#e5e7eb' },
                            title: { display: true, text: 'Price (USD)' }
                        },
                        x: {
                            grid: { display: false },
                            ticks: { 
                                maxTicksLimit: 10, // Limit ticks to keep the axis clean
                                autoSkip: true,
                            }
                        }
                    },
                    interaction: {
                        mode: 'index',
                        intersect: false,
                    },
                    tooltips: {
                        callbacks: {
                            label: function(tooltipItem, data) {
                                return formatCurrency(tooltipItem.raw);
                            }
                        }
                    }
                }
            });
        }
        
        // Attach global function to the window object
        window.runPrediction = runPrediction;
    </script>
</body>
</html>
