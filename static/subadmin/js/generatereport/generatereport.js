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
            console.log(room);
            

            $("#CRUDroom .modal-content").html(data.html_list);
            document.getElementById("room-home").innerHTML="<option value="+room+">"+room+"</option>";
        }
    })
    
}
// function saveGenerate(){
//     var form = $(this)
//     var room = document.getElementById("building-and-room").innerHTML
//     // console.log(form)
//     $.ajax({
//         url:form.attr("action"),
//         data:form.serialize()+'&room='+room,
//         type:form.attr("method"),
//         dataType:'json',
//         success:function(data){
//             console.log(form.serialize());
//             if (data.form_is_valid){
//                 // $(".content-card").html(data.html_list);
//                 $("#CRUDroom").modal("hide");
                
//             }
//             else{
//                 $("#CRUDroom .modal-content").html(data.html_list);
//             }

//         }
//     });
//     return false;
// };


$('.js-weekly').on('click', loadGenerate);
$('.js-monthly').on('click',loadGenerate);
$('.js-annually').on('click',loadGenerate);
// $("#CRUDroom").on('submit','.js-weekly-report',saveGenerate);
// $("#CRUDroom").on('submit','.js-monthly-report',saveGenerate);
// $("#CRUDroom").on('submit','.js-annually-report',saveGenerate);