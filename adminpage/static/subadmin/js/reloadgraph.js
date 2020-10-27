var endpoint;
var dataurl;
$(".content-card .js-load").click(function(){


endpoint = $(this).attr("id");
document.getElementById("building-and-room").innerHTML=endpoint;
dataurl = endpoint+'/request/';
function livegraph(){
    $.ajax({
    url:dataurl,
    method:'GET',
    dataType:'json',
    success:function(data){
        console.log(dataurl)
        if(data.temperature && data.date_and_time){
        var dataSet = data.date_and_time;
        var label = data.temperature;
        chart.data.datasets[0].data=label.reverse();
        chart.data.labels = dataSet.reverse();
        chart.update();
        }else{
            var dataSet ='';
            var label ='';
            chart.data.datasets[0].data=label;
            chart.data.labels = dataSet;
            chart.update();
        }
        
    }, 
 
}
);

}
// document.getElementById("myModal").style.display="none"; 
setInterval(livegraph,1000);


} );      
var center;
var ctx = document.getElementById('myChart').getContext('2d');
var chart = new Chart(ctx, {
// The type of chart we want to create
    type: 'line',

// The data for our dataset
    data: {
        labels: [],
        datasets: [{
            label: 'Temperature',
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
