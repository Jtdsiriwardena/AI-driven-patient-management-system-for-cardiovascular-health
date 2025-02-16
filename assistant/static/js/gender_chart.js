fetch('/data')
.then(response => response.json())
.then(data => {

    // Function to generate a pie chart
    function generatePieChart(canvasId, category, maleCount, femaleCount) {
        var ctx = document.getElementById(canvasId).getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['Male', 'Female'],
                datasets: [
                    {
                        data: [maleCount, femaleCount],
                        backgroundColor: [
                            'rgba(54, 162, 235, 1)', // Male color blue
                            'rgba(255, 99, 132, 1)' // Female color pink
                        ]
                    }
                ]
            },
            options: {
                maintainAspectRatio: true,
                responsive: false, 
                plugins: {}
            }
        });
    }

    // pie charts for each class
    generatePieChart('normalPieChartCanvas', 'normal', data.male_counts[0], data.female_counts[0]);
    generatePieChart('historyOfMiPieChartCanvas', 'history_of_mi', data.male_counts[1], data.female_counts[1]);
    generatePieChart('arrhythmiaPieChartCanvas', 'arrhythmia', data.male_counts[2], data.female_counts[2]);
    generatePieChart('myocardialInfarctionPieChartCanvas', 'myocardial_infarction', data.male_counts[3], data.female_counts[3]);
});
