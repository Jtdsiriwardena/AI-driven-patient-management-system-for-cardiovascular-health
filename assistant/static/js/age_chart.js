
// Fetch age distribution data from the backend
fetch('/age_distribution')
  .then(response => response.json())
  .then(data => {

    // Create bar charts for each table
    createBarChart(data.age_ranges, data.age_counts.arrhythmia, 'arrhythmiaChart', 'Arrhythmia');
    createBarChart(data.age_ranges, data.age_counts.normal, 'normalChart', 'Normal');
    createBarChart(data.age_ranges, data.age_counts.myocardial_infarction, 'myocardialInfarctionChart', 'Myocardial Infarction');
    createBarChart(data.age_ranges, data.age_counts.history_of_mi, 'historyOfMIChart', 'History of MI');
  })
  .catch(error => console.error('Error fetching age distribution data:', error));

// Function to create bar chart
function createBarChart(labels, data, canvasId, title) {
  var ctx = document.getElementById(canvasId).getContext('2d');
  
  // colors for different age groups
  var colors = [
    'rgba(255, 99, 132, 1)', // Red
    'rgba(54, 162, 235, 1)', // Blue
    'rgba(255, 206, 86, 1)', // Yellow
    'rgba(75, 192, 192, 1)', // Green
    'rgba(153, 102, 255, 1)', // Purple
    'rgba(255, 159, 64, 1)', // Orange
    'rgba(231, 233, 237, 1)', // Gray
    'rgba(255, 205, 86, 1)', // Gold
    'rgba(54, 162, 235, 1)', // Blue 
    'rgba(75, 192, 192, 1)' // Green
  ];
  
  var chart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: title,
        data: data,
        backgroundColor: colors.slice(0, data.length), // Assign colors to bars
        borderColor: colors.slice(0, data.length).map(color => color.replace('1', '1')), // border colors
        borderWidth: 1
      }]
    },
    options: {
      plugins: {
      legend: {
          display: false // Hide the legend
      }
  },
      
  scales: {
    y: {
        beginAtZero: true,
        ticks: {
            color: 'rgba(0, 0, 0, 1)', // y-axis label color to white with opacity 1
            font: {
                weight: 'bold', // font weight to bold
                size: 12, // font size
                family: 'Arial' // font family 
            }
        }
    },
    x: {
        ticks: {
            color: 'rgba(0, 0, 0, 1)', // x-axis label color to white with opacity 1
            font: {
                weight: 'bold', // font weight to bold
                size: 12, //  font size to 14px
                family: 'Arial' //  font family 
            }
        }
    }
}

    }
    
  });
}
