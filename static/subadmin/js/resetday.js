var resetperday = function(){
    $.ajax({
        url:'/resetperday/',
        method:'GET',
        success:function(data){

        }
    })
}
setInterval(resetperday,24*3600*1000)
// setInterval(resetperday,7000)