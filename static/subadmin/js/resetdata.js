

var resetdataperhour = function(){
    $.ajax({
        url:'/resetperhour/',
        method:'POST',
        
        success:function(data){

        }
    })
}
var resetperday = function(){
    $.ajax({
        url:'/resetperday/',
        method:'POST',
        success:function(data){

        }
    })
}
setInterval(resetdataperhour,3600*1000)
setInterval(resetperday,24*3600*1000)