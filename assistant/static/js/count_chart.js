
//------------------Display total count-----------------------------//

document.addEventListener('DOMContentLoaded', function () {
    // Define default end date (today)
    var endDate = new Date();
    
    // Define start date as the beginning of data 
    var startDate = new Date('2020-01-01');

    // Format start and end dates as 'YYYY-MM-DD'
    var startDateString = startDate.toISOString().split('T')[0];
    var endDateString = endDate.toISOString().split('T')[0];

    // Call updateChart with default dates
    updateChart(startDateString, endDateString);

    // Fetch and display total count
    fetchTotalCount(startDateString, endDateString);

    // event listener to start and end date input fields
    document.getElementById('start-date').addEventListener('change', function() {
        var startDate = this.value;
        var endDate = document.getElementById('end-date').value;
        updateChart(startDate, endDate);
    });

    document.getElementById('end-date').addEventListener('change', function() {
        var startDate = document.getElementById('start-date').value;
        var endDate = this.value;
        updateChart(startDate, endDate);
    });
});






  //--------------------Filter with date range-----------------//

function updateChart(startDate, endDate) {
    // Check if start date and end date are not empty
    if (startDate && endDate) {

        // Destroy existing chart if it exists
        var existingChart = Chart.getChart("barChart");
        if (existingChart) {
            existingChart.destroy();
        }

        // Make an AJAX request to fetch data from the Flask route with the entered date range
        fetch(`/get_data?start_date=${startDate}&end_date=${endDate}`)
            .then(response => response.json())
            .then(data => {

                // Extract counts from the response
                var counts = Object.values(data);

                // Render the chart
                var ctx = document.getElementById('barChart').getContext('2d');
                var barChart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: Object.keys(data), // Use keys as labels
                        datasets: [{
                            data: counts,
                            backgroundColor: [
                                'rgba(255, 99, 132, 1)', //pink
                                'rgba(54, 162, 235, 1)', //blue
                                'rgba(255, 206, 86, 1)', //yellow
                                'rgba(75, 192, 192, 1)'
                            ],
                            borderColor: [
                                'rgba(255, 99, 132, 1)',
                                'rgba(54, 162, 235, 1)',
                                'rgba(255, 206, 86, 1)',
                                'rgba(75, 192, 192, 1)'
                            ],
                            borderWidth: 1
                        }]
                    },
                    options: {
                        plugins: {
                            legend: {
                                display: false // Hide the legend
                            },
                            
                        },
                        scales: {
                            y: {
                                beginAtZero: true,
                                ticks: {
                                    color: 'rgba(0, 0, 0, 1)', // Set y-axis label color to black
                                    font: {
                                        weight: 'bold', // font weight to bold
                                        size: 16, // font size to 16px
                                        family: 'Arial' // font family if needed
                                    }
                                }
                            },
                            
                        },
                        
                        maintainAspectRatio: false, 
                        responsive: false, 
                        width: 300, // not working changed with html code
                        height: 400, // not working--------------
                        layout: {
                            padding: {
                                left: 20,
                                right: 20,
                                top: 20,
                                bottom: 20
                            }
                        },

                    }
                    
                });
                


    //--------------------Display total count as a number-----------------//

                // Display count in the date range below the button
                var countText = `Count from ${startDate} to ${endDate}: ${counts.reduce((a, b) => a + b, 0)}`;
                
                document.getElementById('date-range-count').innerText = countText;
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });

        // Fetch and display total count
        fetchTotalCount(startDate, endDate);
    } 
    else {
        // Handle case where start date or end date is empty
        console.error('Start date or end date is empty.');
    }
}

function fetchTotalCount(startDate, endDate) {
    // Make an AJAX request to fetch total count from the Flask route with the selected date range
    fetch(`/get_total_count?start_date=${startDate}&end_date=${endDate}`)
        .then(response => response.json())
        .then(totalCount => {
            // Display total count
            document.getElementById('total-count').innerText = `Total Count: ${totalCount}`;
        })
        .catch(error => {
            console.error('Error fetching total count:', error);
        });
}
