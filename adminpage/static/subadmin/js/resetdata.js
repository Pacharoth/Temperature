

var resetdataperhour = function(){
    $.ajax({
        url:'/resetperhour/',
        method:'GET',
        
        success:function(data){

        }
    })
}

setInterval(resetdataperhour,3600*1000);
// setInterval(resetdataperhour,10000)
// setInterval(resetperday,24*3600*1000)