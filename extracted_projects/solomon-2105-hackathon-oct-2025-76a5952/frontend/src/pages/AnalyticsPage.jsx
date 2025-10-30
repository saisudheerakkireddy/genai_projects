import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Plot from 'react-plotly.js'; // Plotly is used for charts
import './AnalyticsPage.css'; // Your existing styles

const API_URL = "http://localhost:5000";

// Helper function to get the start of the week (Sunday) for a given date
function getStartOfWeek(date) {
  const dt = new Date(date);
  const day = dt.getDay(); // 0 = Sunday, 1 = Monday, ...
  const diff = dt.getDate() - day; // Adjust to Sunday
  return new Date(dt.setDate(diff)).toISOString().split('T')[0]; // Return YYYY-MM-DD
}

function AnalyticsPage({ user }) {
  const [allData, setAllData] = useState([]); // Store all fetched data
  const [filteredData, setFilteredData] = useState([]); // Data to display (potentially filtered)
  const [loading, setLoading] = useState(true);
  const [selectedSubjectFilter, setSelectedSubjectFilter] = useState(null); // <-- NEW state for filtering

  useEffect(() => {
    // Fetch all test results for the user
    axios.get(`${API_URL}/api/analytics?username=${user}`)
      .then(response => {
        const parsedData = response.data.map(item => ({
          ...item,
          test_date: new Date(item.test_date)
        }));
        // Sort data by date, newest first (for table initially)
        parsedData.sort((a, b) => b.test_date - a.test_date);
        setAllData(parsedData); // Store the raw data
        setFilteredData(parsedData); // Initially, show all data
        setLoading(false);
      })
      .catch(error => {
        console.error("Error fetching analytics:", error);
        setAllData([]);
        setFilteredData([]);
        setLoading(false);
      });
  }, [user]);

  // --- NEW: Function to handle pie chart clicks ---
  const handlePieClick = (event) => {
    if (event.points && event.points.length > 0) {
      const clickedSubject = event.points[0].label;
      setSelectedSubjectFilter(clickedSubject); // Set the filter
      // Filter the data based on the clicked subject
      const newFilteredData = allData.filter(item => item.subject === clickedSubject);
      setFilteredData(newFilteredData);
    }
  };

  // --- NEW: Function to reset the filter ---
  const resetFilter = () => {
    setSelectedSubjectFilter(null);
    setFilteredData(allData); // Show all data again
  };


  if (loading) {
    return <h1>Loading your analytics...</h1>;
  }

  if (allData.length === 0) { // Check allData for the initial message
    return <h1>No test data found. Go take some tests!</h1>;
  }

  // --- Process Data for Charts and Table (using filteredData) ---

  // 1. For Pie Chart (Tests Attempted per Subject) - Uses allData
  const subjectCounts = {};
  allData.forEach(d => {
    subjectCounts[d.subject] = (subjectCounts[d.subject] || 0) + 1;
  });
  const pieLabels = Object.keys(subjectCounts);
  const pieValues = Object.values(subjectCounts);
  const pieChartData = [{
    values: pieValues, labels: pieLabels, type: 'pie', hole: .4,
    hoverinfo: 'label+percent', textinfo: 'value', textfont_size: 20,
    marker: { line: { color: '#000000', width: 1 } }
  }];

  // 2. For Line Chart (Weekly Average Score) - Uses filteredData
  const weeklyScores = {};
  filteredData.forEach(d => { // Use filteredData here
    const weekStart = getStartOfWeek(d.test_date);
    if (!weeklyScores[weekStart]) {
      weeklyScores[weekStart] = { scores: [], count: 0 };
    }
    weeklyScores[weekStart].scores.push(d.score);
    weeklyScores[weekStart].count++;
  });
  const weeklyAverages = Object.entries(weeklyScores).map(([weekStart, data]) => ({
    week: weekStart,
    averageScore: data.scores.reduce((sum, score) => sum + score, 0) / data.count
  }));
  weeklyAverages.sort((a, b) => new Date(a.week) - new Date(b.week)); // Sort oldest first
  const lineChartData = [
    {
      x: weeklyAverages.map(d => d.week),
      y: weeklyAverages.map(d => d.averageScore),
      type: 'scatter', mode: 'lines+markers', marker: { color: '#4a69bd' },
      line: { shape: 'spline' }
    }
  ];

  // 3. Data for the History Table - Uses filteredData

  return (
    <div className="analytics-page">
      <h1>📊 Your Analytics</h1>

      {/* --- Pie Chart Section (Now clickable) --- */}
      <h2>Tests Attempted per Subject</h2>
       <p className="chart-instruction">Click a subject on the chart to filter the data below.</p>
      <Plot
        data={pieChartData}
        layout={{ title: 'Breakdown of Tests Taken', showlegend: true, height: 400, width: 500 }}
        useResizeHandler={true}
        style={{ width: '100%', maxWidth: '500px', margin: '0 auto 20px auto' }}
        onClick={handlePieClick} // <-- ADDED onClick handler
      />

       {/* --- NEW: Filter Indicator and Reset Button --- */}
        {selectedSubjectFilter && (
            <div className="filter-info">
                Showing data for: <strong>{selectedSubjectFilter}</strong>
                <button onClick={resetFilter} className="reset-button">Show All Subjects</button>
            </div>
        )}

      {/* Only show line chart and table if there's filtered data */}
      {filteredData.length > 0 ? (
        <>
          {/* --- Line Chart Section (Uses filtered data) --- */}
          <h2>{selectedSubjectFilter ? `${selectedSubjectFilter} ` : ''}Weekly Average Score</h2>
          <div className="chart-container">
            <Plot
              data={lineChartData}
              layout={{
                title: selectedSubjectFilter ? `Your ${selectedSubjectFilter} Score Trend` : 'Your Overall Score Trend (Weekly)',
                xaxis: { title: 'Week Starting On' },
                yaxis: { title: 'Average Score (%)', range: [0, 100] }
              }}
              useResizeHandler={true}
              style={{ width: '100%', height: '400px' }}
              config={{ responsive: true }}
            />
          </div>

          {/* --- History Table Section (Uses filtered data) --- */}
          <h2>{selectedSubjectFilter ? `${selectedSubjectFilter} ` : ''}Test History</h2>
          <div className="history-table-container">
            <table className="history-table">
              <thead>
                <tr>
                  <th>Date</th><th>Topic</th><th>Subject</th><th>Score (%)</th>
                </tr>
              </thead>
              <tbody>
                {filteredData.map((result, index) => ( // Use filteredData here
                  <tr key={result.result_id || index}>
                    <td>{result.test_date.toLocaleDateString()}</td>
                    <td>{result.topic}</td>
                    <td>{result.subject}</td>
                    <td>{result.score.toFixed(0)}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      ) : (
        // Show message if filter results in no data
        selectedSubjectFilter && <h2>No test data found for {selectedSubjectFilter}.</h2>
      )}
    </div>
  );
}
export default AnalyticsPage;