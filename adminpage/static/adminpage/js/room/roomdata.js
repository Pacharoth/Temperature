$(function(){

var pointless;
var id;
    // function load modal form
    var loadForm = function(){
        pointless=$(this).attr("data-url")+"?username="+$(this).attr("id")
        console.log($(this).attr("data-url"),$(this).attr("id"))
        id =$(this).attr("id");
        $.ajax({
            url:pointless,
            type:'get',
            dataType:'json',
            beforeSend:function(){
                $("#CRUDroom .modal-content").html("");
                $("#CRUDroom").modal("show");  
            },
            success:function(data){
                $("#CRUDroom .modal-content").html(data.html_room_form);
                document.getElementsByClassName("js-create-room-form")[0].id=id;
            }
        });
    };

    //save data and return the list of room
    var saveForm = function(){
        var form = $(this)
        console.log(form)
        var point= form.attr("action")
        var datapoint = form.serialize()+"&username="+form.attr("id")
        $.ajax({
            url:point,
            data:datapoint,
            type:form.attr("method"),
            dataType:'json',
            success:function(data){
                console.log(datapoint);
                if (data.form_is_valid){
                    $(".content-card").html(data.html_room_list);
                    $("#CRUDroom").modal("hide");
                }
                else{
                    $("#CRUDroom .modal-content").html(data.html_room_form);
                }

            }
        });
        return false;
    };
    //create the room
    // $('.js-create-room').click(loadForm);
    $("#myMain").on("click",".js-create-room",loadForm)
    $('#CRUDroom').on("submit",".js-create-room-form",saveForm);
    //update room
    // $('.js-update-room').click(loadForm);
    $(".dropdown-menu").on("click",".js-update-room",loadForm)

    $('#CRUDroom').on("submit",'.js-update-room-form',saveForm);

    //delete room
    // $('.js-delete-room').click(loadForm);
    $("#myModal").on("click",".js-delete-room",loadForm)
    $('#CRUDroom').on('submit','.js-delete-room-form',saveForm);

})