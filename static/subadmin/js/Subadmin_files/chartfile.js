var another;
$(".modalf-fake .js-load").click(function(){
    console.log($(this));
    another=$(this).attr("id")
    $.ajax({
        url:'/api/year/?room='+another,
        method:"GET",
        success:(data)=>{
            console.log(data)
            if(data.empty){
                document.getElementById("avg-year").innerHTML =" ";
                document.getElementById("avg-monthly").innerHTML=" ";
            }
            else{
                document.getElementById("avg-year").innerHTML = data.datayear+" (C)";
                document.getElementById("avg-monthly").innerHTML=data.datamonth+ " (C)";
            }
            
        }
    })
})
$(".modalf-fake .js-load").click(function(){

console.log($(this))
another = $(this).attr("id");
document.getElementById("room-number").innerHTML=another;
function livegraph(){
    $.ajax({
    url:'/temperature/api/?room='+another,
    type:'GET',
    dataType:'json',
    success:function(data){
        console.log(data);
        if(data.temperature && data.date_and_time){
        var dataSet = data.date_and_time;
        var label = data.temperature;
        document.getElementById("room-temperature").innerHTML = label[0]+" (C)";
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
setInterval(livegraph,5000);


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
            label:"Temperature",
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
// title: {
//     display: true,
//     position:'left',
// },
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
