var ctx = document.getElementById('myChart').getContext('2d');
var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'line',
    
    // The data for our dataset
    data: {
        labels: [],
        datasets: [{
            label: 'Temperature:',
            backgroundColor: '#deeff5',
            borderColor: '#add8e6',
            hoverBackgroundColor: "rgba(255,99,132,0.4)",
            data: []
        }]
    },

    // Configuration options go here
    options: {
        // maintainAspectRatio: false,
        responsiveAnimationDuration:0,
        // aspectRatio:2,
        // onResize:null,
        responsive:true,
        title: {
            display: true,
            position:'left',
            text: 'Celsius'
        },
        scales: {
            xAxes: [{
                display: true
            }],
            yAxes: [{
               
                display: true
            }]
        },
        legend: {
            display: true,
            labels: {
                
            }
        }
        
    }
});

