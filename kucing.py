<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gemini Data Explorer</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.3.2/papaparse.min.js"></script>
    <script src="https://cdn.plot.ly/plotly-2.24.1.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Orbitron:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #0f0c29; /* Deep space blue */
            color: #e0e0e0; /* Light gray for text */
            overflow-x: hidden;
        }
        .cosmic-bg {
            background: linear-gradient(to bottom right, #0f0c29, #302b63, #24243e); /* Cosmic gradient */
        }
        .header-font {
            font-family: 'Orbitron', sans-serif;
        }
        .card {
            background-color: rgba(22, 28, 58, 0.7); /* Translucent dark blue */
            backdrop-filter: blur(5px);
            border: 1px solid rgba(76, 89, 166, 0.5); /* Nebula purple border */
            border-radius: 12px;
            box-shadow: 0 8px 32px 0 rgba(116, 76, 166, 0.37); /* Soft purple glow */
        }
        .filter-select, .filter-input {
            background-color: rgba(36, 36, 62, 0.8);
            border: 1px solid rgba(76, 89, 166, 0.6);
            color: #e0e0e0;
            border-radius: 8px;
        }
        .filter-select:focus, .filter-input:focus {
            outline: none;
            border-color: #9f7aea; /* Brighter purple on focus */
            box-shadow: 0 0 0 2px rgba(159, 122, 234, 0.4);
        }
        .btn-primary {
            background: linear-gradient(to right, #6a11cb, #2575fc); /* Purple to blue gradient */
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px 0 rgba(106, 17, 203, 0.5);
        }
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px 0 rgba(37, 117, 252, 0.6);
        }
        .chart-container {
            min-height: 350px; /* Ensure space for charts */
        }
        .insight-loading, .insight-error {
            color: #facc15; /* Amber for loading/error */
        }
        .insight-item {
            background-color: rgba(40, 40, 70, 0.5);
            padding: 8px;
            border-radius: 6px;
            margin-bottom: 6px;
            border-left: 3px solid #8b5cf6; /* Purple accent */
        }
        /* Custom scrollbar for a more thematic feel */
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #1e1b4b; /* Dark indigo */
        }
        ::-webkit-scrollbar-thumb {
            background: #4f46e5; /* Indigo */
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #6366f1; /* Lighter indigo */
        }
        .loader {
            border: 4px solid #302b63; /* Lighter part of gradient */
            border-top: 4px solid #8b5cf6; /* Purple */
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        #mainLoader {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.7);
            z-index: 9999;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
        }
        #mainLoaderText {
            color: white;
            margin-top: 10px;
            font-size: 1.2em;
        }
    </style>
</head>
<body class="cosmic-bg min-h-screen p-4 md:p-8">

    <div id="mainLoader" class="hidden">
        <div class="loader"></div>
        <p id="mainLoaderText">Processing...</p>
    </div>

    <header class="text-center mb-8 md:mb-12">
        <h1 class="text-4xl md:text-5xl font-bold header-font text-transparent bg-clip-text bg-gradient-to-r from-purple-400 via-pink-400 to-red-400">
            🌌 Gemini Data Explorer 🌠
        </h1>
        <p class="text-lg text-purple-300 mt-2">Upload your CSV and unlock cosmic insights!</p>
    </header>

    <div class="card p-6 mb-8">
        <h2 class="text-2xl font-semibold mb-4 text-purple-300">🚀 Launch Your Analysis</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 items-end">
            <div>
                <label for="csvFile" class="block mb-2 text-sm font-medium text-gray-300">Upload CSV File:</label>
                <input type="file" id="csvFile" accept=".csv" class="block w-full text-sm text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-violet-700 file:text-violet-50 hover:file:bg-violet-600 transition-colors duration-150 cursor-pointer">
            </div>
            <button id="analyzeButton" class="btn-primary h-10 md:mt-0 mt-4">Analyze Data</button>
        </div>
        <div id="fileError" class="text-red-400 mt-2 text-sm"></div>
        <div id="columnInfo" class="text-amber-400 mt-2 text-sm"></div>

    </div>

    <div class="card p-6 mb-8">
        <h2 class="text-2xl font-semibold mb-4 text-purple-300">🔭 Filter Your Universe</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            <div>
                <label for="platformFilter" class="block mb-1 text-sm text-gray-300">Platform:</label>
                <select id="platformFilter" class="filter-select w-full p-2"></select>
            </div>
            <div>
                <label for="sentimentFilter" class="block mb-1 text-sm text-gray-300">Sentiment:</label>
                <select id="sentimentFilter" class="filter-select w-full p-2"></select>
            </div>
            <div>
                <label for="mediaTypeFilter" class="block mb-1 text-sm text-gray-300">Media Type:</label>
                <select id="mediaTypeFilter" class="filter-select w-full p-2"></select>
            </div>
            <div>
                <label for="locationFilter" class="block mb-1 text-sm text-gray-300">Location:</label>
                <select id="locationFilter" class="filter-select w-full p-2"></select>
            </div>
            <div>
                <label for="startDateFilter" class="block mb-1 text-sm text-gray-300">Start Date:</label>
                <input type="date" id="startDateFilter" class="filter-input w-full p-2">
            </div>
            <div>
                <label for="endDateFilter" class="block mb-1 text-sm text-gray-300">End Date:</label>
                <input type="date" id="endDateFilter" class="filter-input w-full p-2">
            </div>
        </div>
    </div>

    <div id="dashboard" class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div id="sentimentChartCard" class="card p-4 hidden">
            <h3 class="text-xl font-semibold mb-3 text-purple-300">Sentiment Breakdown</h3>
            <div id="sentimentChart" class="chart-container"></div>
            <div class="mt-3">
                <h4 class="text-md font-semibold text-purple-400 mb-1">Insights:</h4>
                <div id="sentimentInsights" class="text-sm space-y-1"></div>
            </div>
        </div>

        <div id="engagementTrendChartCard" class="card p-4 hidden">
            <h3 class="text-xl font-semibold mb-3 text-purple-300">Engagement Trend Over Time</h3>
            <div id="engagementTrendChart" class="chart-container"></div>
            <div class="mt-3">
                <h4 class="text-md font-semibold text-purple-400 mb-1">Insights:</h4>
                <div id="engagementTrendInsights" class="text-sm space-y-1"></div>
            </div>
        </div>

        <div id="platformEngagementsChartCard" class="card p-4 hidden">
            <h3 class="text-xl font-semibold mb-3 text-purple-300">Platform Engagements</h3>
            <div id="platformEngagementsChart" class="chart-container"></div>
            <div class="mt-3">
                <h4 class="text-md font-semibold text-purple-400 mb-1">Insights:</h4>
                <div id="platformEngagementsInsights" class="text-sm space-y-1"></div>
            </div>
        </div>

        <div id="mediaTypeMixChartCard" class="card p-4 hidden">
            <h3 class="text-xl font-semibold mb-3 text-purple-300">Media Type Mix</h3>
            <div id="mediaTypeMixChart" class="chart-container"></div>
            <div class="mt-3">
                <h4 class="text-md font-semibold text-purple-400 mb-1">Insights:</h4>
                <div id="mediaTypeMixInsights" class="text-sm space-y-1"></div>
            </div>
        </div>

        <div id="topLocationsChartCard" class="card p-4 hidden">
            <h3 class="text-xl font-semibold mb-3 text-purple-300">Top 5 Locations</h3>
            <div id="topLocationsChart" class="chart-container"></div>
            <div class="mt-3">
                <h4 class="text-md font-semibold text-purple-400 mb-1">Insights:</h4>
                <div id="topLocationsInsights" class="text-sm space-y-1"></div>
            </div>
        </div>
         <div id="dataOverviewCard" class="card p-4 hidden lg:col-span-2">
            <h3 class="text-xl font-semibold mb-3 text-purple-300">Data Overview</h3>
            <p id="dataRowCount" class="text-gray-300"></p>
            <div id="dataSample" class="overflow-x-auto mt-2">
                <table class="min-w-full text-sm text-left text-gray-400">
                    <thead id="dataSampleHeader" class="text-xs text-gray-300 uppercase bg-gray-700/50"></thead>
                    <tbody id="dataSampleBody" class="bg-gray-800/50"></tbody>
                </table>
            </div>
        </div>
    </div>

    <footer class="text-center mt-12 pb-4">
        <p class="text-sm text-gray-500">Powered by Gemini & Plotly.js</p>
    </footer>

    <script>
        // DOM Elements
        const csvFileInput = document.getElementById('csvFile');
        const analyzeButton = document.getElementById('analyzeButton');
        const fileErrorDiv = document.getElementById('fileError');
        const columnInfoDiv = document.getElementById('columnInfo');
        const mainLoader = document.getElementById('mainLoader');
        const mainLoaderText = document.getElementById('mainLoaderText');

        const platformFilter = document.getElementById('platformFilter');
        const sentimentFilter = document.getElementById('sentimentFilter');
        const mediaTypeFilter = document.getElementById('mediaTypeFilter');
        const locationFilter = document.getElementById('locationFilter');
        const startDateFilter = document.getElementById('startDateFilter');
        const endDateFilter = document.getElementById('endDateFilter');

        const chartCards = {
            sentiment: document.getElementById('sentimentChartCard'),
            engagementTrend: document.getElementById('engagementTrendChartCard'),
            platformEngagements: document.getElementById('platformEngagementsChartCard'),
            mediaTypeMix: document.getElementById('mediaTypeMixChartCard'),
            topLocations: document.getElementById('topLocationsChartCard'),
        };
        const dataOverviewCard = document.getElementById('dataOverviewCard');


        let originalData = [];
        let processedData = [];
        // Standard column names, user will be asked to map if not found
        const EXPECTED_COLUMNS = {
            date: "Date",
            engagements: "Engagements",
            sentiment: "Sentiment",
            platform: "Platform",
            mediaType: "Media Type",
            location: "Location"
        };
        let actualColumnNames = { ...EXPECTED_COLUMNS }; // Will be updated after header detection

        const PLOTLY_LAYOUT_CONFIG = {
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            font: { color: '#e0e0e0' },
            legend: { orientation: 'h', yanchor: 'bottom', y: 1.02, xanchor: 'right', x: 1 },
            margin: { l: 50, r: 20, b: 50, t: 50, pad: 4 } // Adjusted margins
        };
        const PLOTLY_PIE_COLORS = ['#9333ea', '#ec4899', '#f97316', '#10b981', '#3b82f6', '#facc15'];


        function showLoader(text = "Processing...") {
            mainLoaderText.textContent = text;
            mainLoader.classList.remove('hidden');
        }

        function hideLoader() {
            mainLoader.classList.add('hidden');
        }
        
        analyzeButton.addEventListener('click', handleFileUpload);
        [platformFilter, sentimentFilter, mediaTypeFilter, locationFilter, startDateFilter, endDateFilter].forEach(filter => {
            filter.addEventListener('change', () => {
                if (originalData.length > 0) {
                     showLoader("Applying filters and updating dashboard...");
                     setTimeout(() => { // Timeout to allow loader to show
                        renderDashboard();
                        hideLoader();
                    }, 50);
                }
            });
        });

        function handleFileUpload() {
            const file = csvFileInput.files[0];
            fileErrorDiv.textContent = '';
            columnInfoDiv.textContent = '';

            if (!file) {
                fileErrorDiv.textContent = 'Please select a CSV file.';
                return;
            }
            if (!file.name.endsWith('.csv')) {
                fileErrorDiv.textContent = 'Invalid file type. Please upload a .csv file.';
                return;
            }

            showLoader("Parsing CSV file...");

            Papa.parse(file, {
                header: true,
                skipEmptyLines: true,
                complete: (results) => {
                    if (results.errors.length > 0) {
                        fileErrorDiv.textContent = `Error parsing CSV: ${results.errors[0].message}`;
                        console.error("CSV Parsing Errors:", results.errors);
                        hideLoader();
                        return;
                    }
                    originalData = results.data;
                    actualColumnNames = findActualColumnNames(results.meta.fields);
                    
                    const missingColumns = Object.keys(EXPECTED_COLUMNS).filter(key => !actualColumnNames[key]);
                    if (missingColumns.length > 0) {
                        columnInfoDiv.innerHTML = `Warning: Could not automatically find columns for: <strong>${missingColumns.join(', ')}</strong>. 
                                                Using default names or first available. Please ensure your CSV has headers like: 
                                                '${Object.values(EXPECTED_COLUMNS).join("', '")}'. 
                                                Charts might not display correctly if essential columns (Date, Engagements) are missing or misnamed.`;
                    } else {
                         columnInfoDiv.textContent = "Successfully mapped all expected columns.";
                    }

                    cleanData();
                    populateFilters();
                    renderDashboard();
                    Object.values(chartCards).forEach(card => card.classList.remove('hidden'));
                    dataOverviewCard.classList.remove('hidden');
                    hideLoader();
                },
                error: (error) => {
                    fileErrorDiv.textContent = `Error reading file: ${error.message}`;
                    hideLoader();
                }
            });
        }

        function findActualColumnNames(csvHeaders) {
            const foundNames = {};
            const lowerCsvHeaders = csvHeaders.map(h => h.toLowerCase().trim());

            for (const key in EXPECTED_COLUMNS) {
                const expected = EXPECTED_COLUMNS[key].toLowerCase();
                const foundIndex = lowerCsvHeaders.findIndex(h => h.includes(expected) || expected.includes(h));
                if (foundIndex !== -1) {
                    foundNames[key] = csvHeaders[foundIndex];
                } else {
                    // Fallback: if a specific key is not found, try to assign a default or leave it undefined
                    // For essential columns like 'date' and 'engagements', this could be an issue.
                    console.warn(`Could not find a column for "${EXPECTED_COLUMNS[key]}". Trying to use default or first available if critical.`);
                    // A more robust solution might involve asking the user to map columns.
                    // For now, we'll rely on the user having reasonably named columns.
                    if (key === 'date' && !foundNames[key]) foundNames[key] = csvHeaders.find(h => h.toLowerCase().includes('date'));
                    if (key === 'engagements' && !foundNames[key]) foundNames[key] = csvHeaders.find(h => h.toLowerCase().includes('engage'));
                }
            }
            return foundNames;
        }


        function cleanData() {
            showLoader("Cleaning data...");
            processedData = originalData.map(row => {
                const dateCol = actualColumnNames.date || 'Date'; // Use detected or default
                const engagementsCol = actualColumnNames.engagements || 'Engagements';

                let date = new Date(row[dateCol]);
                if (isNaN(date.getTime())) { // Try to parse common non-standard formats
                    const parts = (row[dateCol] || "").match(/(\d{1,2})[\/\-\.](\d{1,2})[\/\-\.](\d{2,4})/);
                    if (parts) {
                        // Assuming DD/MM/YYYY or MM/DD/YYYY - this is ambiguous. Prioritize MM/DD/YYYY for broader compatibility.
                        // For more robust parsing, a date library like moment.js or date-fns would be better.
                        const year = parseInt(parts[3].length === 2 ? '20' + parts[3] : parts[3]);
                        const month = parseInt(parts[1]) -1; // JS months are 0-indexed
                        const day = parseInt(parts[2]);
                        date = new Date(year, month, day);
                        if (isNaN(date.getTime())) { // If still invalid, try swapping month and day
                             date = new Date(year, parseInt(parts[2])-1, parseInt(parts[1]));
                        }
                    }
                }
                 if (isNaN(date.getTime())) { // If still invalid, set to null or keep original string
                    console.warn(`Invalid date format for value: ${row[dateCol]}. Setting to null.`);
                    date = null;
                }


                return {
                    ...row,
                    [dateCol]: date,
                    [engagementsCol]: parseFloat(row[engagementsCol]) || 0
                };
            }).filter(row => row[actualColumnNames.date || 'Date'] instanceof Date); // Ensure only valid dates proceed
            hideLoader();
        }

        function populateFilters() {
            showLoader("Populating filters...");
            const filtersToPopulate = [
                { el: platformFilter, columnKey: 'platform' },
                { el: sentimentFilter, columnKey: 'sentiment' },
                { el: mediaTypeFilter, columnKey: 'mediaType' },
                { el: locationFilter, columnKey: 'location' }
            ];

            filtersToPopulate.forEach(f => {
                const columnName = actualColumnNames[f.columnKey];
                if (!columnName) {
                    console.warn(`Column for ${f.columnKey} filter not found.`);
                    f.el.innerHTML = '<option value="">N/A</option>';
                    return;
                }
                const uniqueValues = [...new Set(processedData.map(row => row[columnName]).filter(Boolean))].sort();
                f.el.innerHTML = '<option value="">All</option>';
                uniqueValues.forEach(val => {
                    const option = document.createElement('option');
                    option.value = val;
                    option.textContent = val;
                    f.el.appendChild(option);
                });
            });

            // Populate date filters with min/max dates from data
            const dateCol = actualColumnNames.date || 'Date';
            const dates = processedData.map(row => row[dateCol]).filter(d => d instanceof Date);
            if (dates.length > 0) {
                const minDate = new Date(Math.min(...dates));
                const maxDate = new Date(Math.max(...dates));
                startDateFilter.value = minDate.toISOString().split('T')[0];
                endDateFilter.value = maxDate.toISOString().split('T')[0];
            }
            hideLoader();
        }

        function getFilteredData() {
            let data = [...processedData];

            const platformVal = platformFilter.value;
            const sentimentVal = sentimentFilter.value;
            const mediaTypeVal = mediaTypeFilter.value;
            const locationVal = locationFilter.value;
            const startDateVal = startDateFilter.value ? new Date(startDateFilter.value) : null;
            const endDateVal = endDateFilter.value ? new Date(endDateFilter.value) : null;
            
            if (startDateVal) startDateVal.setHours(0,0,0,0); // Normalize to start of day
            if (endDateVal) endDateVal.setHours(23,59,59,999); // Normalize to end of day


            const dateCol = actualColumnNames.date || 'Date';
            const platformCol = actualColumnNames.platform || 'Platform';
            const sentimentCol = actualColumnNames.sentiment || 'Sentiment';
            const mediaTypeCol = actualColumnNames.mediaType || 'Media Type';
            const locationCol = actualColumnNames.location || 'Location';

            return data.filter(row => {
                const rowDate = row[dateCol];
                if (!(rowDate instanceof Date)) return false; // Skip rows with invalid dates

                if (platformVal && columnName && row[platformCol] !== platformVal) return false;
                if (sentimentVal && columnName && row[sentimentCol] !== sentimentVal) return false;
                if (mediaTypeVal && columnName && row[mediaTypeCol] !== mediaTypeVal) return false;
                if (locationVal && columnName && row[locationCol] !== locationVal) return false;
                if (startDateVal && rowDate < startDateVal) return false;
                if (endDateVal && rowDate > endDateVal) return false;
                return true;
            });
        }

        async function renderDashboard() {
            showLoader("Rendering dashboard...");
            const filteredData = getFilteredData();

            if (filteredData.length === 0 && originalData.length > 0) {
                 Object.values(chartCards).forEach(card => {
                    const chartDivId = card.querySelector('.chart-container').id;
                    const insightsDivId = card.querySelector('.text-sm.space-y-1').id;
                    Plotly.purge(chartDivId);
                    document.getElementById(chartDivId).innerHTML = "<p class='text-center text-gray-400 p-8'>No data matches the current filters.</p>";
                    document.getElementById(insightsDivId).innerHTML = "<p class='text-center text-gray-400'>N/A</p>";
                });
                dataOverviewCard.classList.remove('hidden');
                document.getElementById('dataRowCount').textContent = `Displaying 0 of ${processedData.length} rows after filtering.`;
                document.getElementById('dataSampleHeader').innerHTML = '';
                document.getElementById('dataSampleBody').innerHTML = '<tr><td colspan="100%" class="text-center p-4">No data to display.</td></tr>';

                hideLoader();
                return;
            } else if (originalData.length === 0) {
                // No data loaded yet, do nothing or show initial message
                hideLoader();
                return;
            }


            // Display data overview
            dataOverviewCard.classList.remove('hidden');
            document.getElementById('dataRowCount').textContent = `Displaying ${filteredData.length} of ${processedData.length} rows.`;
            const sampleData = filteredData.slice(0, 5);
            const sampleHeader = document.getElementById('dataSampleHeader');
            const sampleBody = document.getElementById('dataSampleBody');
            sampleHeader.innerHTML = '';
            sampleBody.innerHTML = '';

            if (sampleData.length > 0) {
                const headers = Object.keys(sampleData[0]);
                const trHeader = document.createElement('tr');
                headers.forEach(header => {
                    const th = document.createElement('th');
                    th.scope = 'col';
                    th.className = 'px-6 py-3';
                    th.textContent = header;
                    trHeader.appendChild(th);
                });
                sampleHeader.appendChild(trHeader);

                sampleData.forEach(row => {
                    const tr = document.createElement('tr');
                    tr.className = 'border-b border-gray-700';
                    headers.forEach(header => {
                        const td = document.createElement('td');
                        td.className = 'px-6 py-4';
                        let cellValue = row[header];
                        if (cellValue instanceof Date) {
                            cellValue = cellValue.toLocaleDateString();
                        }
                        td.textContent = cellValue !== null && cellValue !== undefined ? cellValue : 'N/A';
                        tr.appendChild(td);
                    });
                    sampleBody.appendChild(tr);
                });
            } else {
                 sampleBody.innerHTML = '<tr><td colspan="100%" class="text-center p-4">No data to display for the current selection.</td></tr>';
            }


            const insightPromises = [];

            // 1. Sentiment Breakdown (Pie Chart)
            const sentimentCol = actualColumnNames.sentiment || 'Sentiment';
            if (filteredData.length > 0 && filteredData[0].hasOwnProperty(sentimentCol)) {
                const sentimentCounts = filteredData.reduce((acc, row) => {
                    const sentiment = row[sentimentCol] || "Unknown";
                    acc[sentiment] = (acc[sentiment] || 0) + 1;
                    return acc;
                }, {});
                const sentimentData = [{
                    labels: Object.keys(sentimentCounts),
                    values: Object.values(sentimentCounts),
                    type: 'pie',
                    marker: { colors: PLOTLY_PIE_COLORS },
                    hoverinfo: 'label+percent',
                    textinfo: 'label+percent'
                }];
                Plotly.newPlot('sentimentChart', sentimentData, { ...PLOTLY_LAYOUT_CONFIG, title: '' }, {responsive: true});
                insightPromises.push(getInsights('sentimentInsights', 'Sentiment Pie Chart', `Sentiment distribution: ${JSON.stringify(sentimentCounts)}`));
                chartCards.sentiment.classList.remove('hidden');
            } else {
                chartCards.sentiment.classList.add('hidden');
            }


            // 2. Engagement Trend over Time (Line Chart)
            const dateCol = actualColumnNames.date || 'Date';
            const engagementsCol = actualColumnNames.engagements || 'Engagements';

            if (filteredData.length > 0 && filteredData[0].hasOwnProperty(dateCol) && filteredData[0].hasOwnProperty(engagementsCol)) {
                const engagementByDate = filteredData.reduce((acc, row) => {
                    const dateStr = row[dateCol].toISOString().split('T')[0];
                    acc[dateStr] = (acc[dateStr] || 0) + row[engagementsCol];
                    return acc;
                }, {});
                const sortedDates = Object.keys(engagementByDate).sort((a,b) => new Date(a) - new Date(b));
                const engagementTrendData = [{
                    x: sortedDates,
                    y: sortedDates.map(date => engagementByDate[date]),
                    type: 'scatter', // 'scatter' for lines
                    mode: 'lines+markers',
                    marker: { color: '#8b5cf6' },
                    line: { shape: 'spline' }
                }];
                Plotly.newPlot('engagementTrendChart', engagementTrendData, { ...PLOTLY_LAYOUT_CONFIG, title: '', xaxis: {type: 'date'} }, {responsive: true});
                const trendSummary = sortedDates.map(date => ({date, engagements: engagementByDate[date]})).slice(-30); // Last 30 points for summary
                insightPromises.push(getInsights('engagementTrendInsights', 'Engagement Trend Line Chart', `Engagement trend data (sample): ${JSON.stringify(trendSummary)}`));
                chartCards.engagementTrend.classList.remove('hidden');
            } else {
                chartCards.engagementTrend.classList.add('hidden');
            }

            // 3. Platform Engagements (Bar Chart)
            const platformCol = actualColumnNames.platform || 'Platform';
             if (filteredData.length > 0 && filteredData[0].hasOwnProperty(platformCol) && filteredData[0].hasOwnProperty(engagementsCol)) {
                const platformEngagements = filteredData.reduce((acc, row) => {
                    const platform = row[platformCol] || "Unknown";
                    acc[platform] = (acc[platform] || 0) + row[engagementsCol];
                    return acc;
                }, {});
                const platformData = [{
                    x: Object.keys(platformEngagements),
                    y: Object.values(platformEngagements),
                    type: 'bar',
                    marker: { color: PLOTLY_PIE_COLORS }
                }];
                Plotly.newPlot('platformEngagementsChart', platformData, { ...PLOTLY_LAYOUT_CONFIG, title: '' }, {responsive: true});
                insightPromises.push(getInsights('platformEngagementsInsights', 'Platform Engagements Bar Chart', `Engagements by platform: ${JSON.stringify(platformEngagements)}`));
                chartCards.platformEngagements.classList.remove('hidden');
            } else {
                chartCards.platformEngagements.classList.add('hidden');
            }


            // 4. Media Type Mix (Pie Chart)
            const mediaTypeCol = actualColumnNames.mediaType || 'Media Type';
            if (filteredData.length > 0 && filteredData[0].hasOwnProperty(mediaTypeCol)) {
                const mediaTypeCounts = filteredData.reduce((acc, row) => {
                    const mediaType = row[mediaTypeCol] || "Unknown";
                    acc[mediaType] = (acc[mediaType] || 0) + 1; // Count of posts by media type
                    return acc;
                }, {});
                const mediaTypeData = [{
                    labels: Object.keys(mediaTypeCounts),
                    values: Object.values(mediaTypeCounts),
                    type: 'pie',
                    marker: { colors: PLOTLY_PIE_COLORS.slice(1) }, // Use different colors
                    hoverinfo: 'label+percent',
                    textinfo: 'label+percent'
                }];
                Plotly.newPlot('mediaTypeMixChart', mediaTypeData, { ...PLOTLY_LAYOUT_CONFIG, title: '' }, {responsive: true});
                insightPromises.push(getInsights('mediaTypeMixInsights', 'Media Type Mix Pie Chart', `Media type distribution: ${JSON.stringify(mediaTypeCounts)}`));
                chartCards.mediaTypeMix.classList.remove('hidden');
            } else {
                chartCards.mediaTypeMix.classList.add('hidden');
            }

            // 5. Top 5 Locations (Bar Chart)
            const locationCol = actualColumnNames.location || 'Location';
            if (filteredData.length > 0 && filteredData[0].hasOwnProperty(locationCol) && filteredData[0].hasOwnProperty(engagementsCol)) {
                const locationEngagements = filteredData.reduce((acc, row) => {
                    const location = row[locationCol] || "Unknown";
                    acc[location] = (acc[location] || 0) + row[engagementsCol];
                    return acc;
                }, {});
                const sortedLocations = Object.entries(locationEngagements)
                    .sort(([,a],[,b]) => b-a)
                    .slice(0, 5);
                const topLocationsData = [{
                    x: sortedLocations.map(([loc, _]) => loc),
                    y: sortedLocations.map(([_, eng]) => eng),
                    type: 'bar',
                    marker: { color: PLOTLY_PIE_COLORS.slice(2) }
                }];
                Plotly.newPlot('topLocationsChart', topLocationsData, { ...PLOTLY_LAYOUT_CONFIG, title: '' }, {responsive: true});
                insightPromises.push(getInsights('topLocationsInsights', 'Top 5 Locations Bar Chart', `Top 5 locations by engagement: ${JSON.stringify(Object.fromEntries(sortedLocations))}`));
                chartCards.topLocations.classList.remove('hidden');
            } else {
                chartCards.topLocations.classList.add('hidden');
            }
            
            await Promise.all(insightPromises);
            hideLoader();
        }

        async function getInsights(elementId, chartName, dataSummary) {
            const insightDiv = document.getElementById(elementId);
            insightDiv.innerHTML = '<div class="insight-loading p-2">🌌 Generating cosmic insights...</div>';

            const prompt = `You are a data analyst. Based on the following data from a "${chartName}", provide exactly 3 concise and distinct insights. Each insight should be a short sentence or two. Data: ${dataSummary}. Format insights as a list.`;
            
            let chatHistory = [{ role: "user", parts: [{ text: prompt }] }];
            const payload = { contents: chatHistory };
            const apiKey = ""; // Will be auto-filled by the environment
            const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`;

            try {
                const response = await fetch(apiUrl, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    console.error("Gemini API Error Response:", errorData);
                    throw new Error(`API request failed with status ${response.status}: ${errorData?.error?.message || response.statusText}`);
                }

                const result = await response.json();

                if (result.candidates && result.candidates.length > 0 &&
                    result.candidates[0].content && result.candidates[0].content.parts &&
                    result.candidates[0].content.parts.length > 0) {
                    const text = result.candidates[0].content.parts[0].text;
                    // Process text to be bullet points or numbered list
                    const insightsArray = text.split('\n').map(item => item.trim().replace(/^[\*\-\d\.]+\s*/, '')).filter(item => item.length > 0);
                    
                    if (insightsArray.length > 0) {
                        insightDiv.innerHTML = insightsArray.map(insight => `<div class="insight-item">${insight}</div>`).join('');
                    } else {
                        insightDiv.innerHTML = '<div class="insight-item">Could not extract insights from the response.</div>';
                    }
                } else {
                    console.error("Unexpected API response structure:", result);
                    insightDiv.innerHTML = '<div class="insight-error">✨ Cosmic interference! Could not generate insights at this moment. Structure issue.</div>';
                }
            } catch (error) {
                console.error('Error fetching insights:', error);
                insightDiv.innerHTML = `<div class="insight-error">✨ Cosmic turbulence! Error fetching insights: ${error.message}. Please check console.</div>`;
            }
        }

        // Initial message if no data is loaded
        function showInitialDashboardMessage() {
            const dashboard = document.getElementById('dashboard');
            let hasVisibleCharts = false;
            Object.values(chartCards).forEach(card => {
                if (!card.classList.contains('hidden')) {
                    hasVisibleCharts = true;
                }
            });

            if (!hasVisibleCharts && originalData.length === 0) {
                 // Clear any existing charts or messages if any
                Object.values(chartCards).forEach(card => {
                    const chartDivId = card.querySelector('.chart-container').id;
                    const insightsDivId = card.querySelector('.text-sm.space-y-1').id;
                    document.getElementById(chartDivId).innerHTML = "";
                    document.getElementById(insightsDivId).innerHTML = "";
                    card.classList.add('hidden'); // Ensure all cards are hidden initially
                });
                dataOverviewCard.classList.add('hidden');

                // Add a placeholder message to the dashboard area if it's empty
                if (dashboard.children.length <= 1) { // Check if only template or empty
                     const placeholder = document.createElement('div');
                     placeholder.className = 'col-span-full text-center py-10 card';
                     placeholder.innerHTML = `<p class="text-xl text-purple-300">✨ Please upload a CSV file to begin your data exploration journey! ✨</p> 
                                              <p class="text-sm text-gray-400 mt-2">Ensure your CSV has columns like: Date, Engagements, Sentiment, Platform, Media Type, Location.</p>`;
                     // Prepend to ensure it's visible if dashboard is empty
                     if (dashboard.firstChild) {
                        dashboard.insertBefore(placeholder, dashboard.firstChild);
                     } else {
                        dashboard.appendChild(placeholder);
                     }
                }
            } else {
                // If charts are visible or data is loaded, remove any initial placeholder
                const existingPlaceholder = dashboard.querySelector('.col-span-full.text-center.py-10.card');
                if (existingPlaceholder) {
                    existingPlaceholder.remove();
                }
            }
        }
        showInitialDashboardMessage(); // Call on page load

    </script>
</body>
</html>
