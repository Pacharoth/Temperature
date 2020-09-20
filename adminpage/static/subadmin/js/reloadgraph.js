$(function(){
    
    var refreshpage=function(){
        var btn=$(this);

        console.log(btn);
        var endpoint = btn.attr("data-store");
        console.log(endpoint)
        var livegraph = function(){
            $.ajax({
            url:endpoint,
            type:"get",
            dataType:'json',
            success:function(data){
                console.log(endpoint);
                console.log(data.temperature);
                console.log(data.date_and_time);
                var dataSet = data.date_and_time;
                var label = data.temperature;
                console.log(label);
                chart.data.datasets[0].data=label;  
                chart.data.labels = dataSet;
                chart.update();
                
            }, 
            complete:function(data){
                setTimeout(livegraph,5000);
            }
        }
        );
        
        }
        livegraph();
        
        // man=setInterval(livegraph,1000);
        
        // livegraph();
        // var clear = clearInterval(setint,20000);
        // clear;
    }
    
    
    
    
            

    $(".js-load").on("click",refreshpage);
    
    
})

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
            data: [],
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
