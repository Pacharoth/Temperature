var report = document.getElementById("room-number").innerHTML
console.log(report)
if (report==""){
    $(".generate-report").hide();
    console.log($(".generate-report"))
    console.log(report)
}
$('.modalf-fake .js-load').click(function(){
    setTimeout(()=>{
        var room =$(this).attr("id");
        if (room!=""){
            $(".generate-report").show();
        }
    },2000)
});
var endpointgener;
function loadGenerateAdmin(){
    var room = document.getElementById("room-number").innerHTML
    endpointgener = $(this).attr("data-url")+'?room='+room;
    $.ajax({
        url:endpointgener,
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


$('.js-weekly').on('click', loadGenerateAdmin);
$('.js-monthly').on('click',loadGenerateAdmin);
$('.js-annually').on('click',loadGenerateAdmin);
// $("#CRUDroom").on('submit','.js-weekly-report',saveGenerate);
// $("#CRUDroom").on('submit','.js-monthly-report',saveGenerate);
// $("#CRUDroom").on('submit','.js-annually-report',saveGenerate);