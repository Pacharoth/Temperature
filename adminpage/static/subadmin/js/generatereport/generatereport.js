var report = document.getElementById("building-and-room").innerHTML
console.log(report)
if (report==""){
    $(".generate-report").hide();
}
$('.js-load').click(function(){
    setTimeout(()=>{
        var room =document.getElementById("building-and-room").innerHTML;
        if (room!=""){
            $(".generate-report").show();
        }
    },2000)
});
var endpointgen;
function loadGenerate(){
   var room = document.getElementById("building-and-room").innerHTML
    endpointgen = $(this).attr("data-url")+'?room='+room;
    $.ajax({
        url:endpointgen,
        method:"GET",
        beforeSend:function(){
            $("#CRUDroom .modal-content").html("")
            $("#CRUDroom").modal("show");
        },
        success:function(data){
            console.log(data);
            $("#CRUDroom .modal-content").html(data.html_list);
           
        }
    })
    
}


$('.js-weekly').on('click', loadGenerate);
$('.js-monthly').on('click',loadGenerate);
$('.js-annually').on('click',loadGenerate);
