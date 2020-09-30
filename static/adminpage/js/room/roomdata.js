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
    //form update and delete
    var urlpoint;
    var idup;
    var loadUpdateAndDelete =function(){
        urlpoint = $(this).attr("data-url")+"?username="+$(this).attr("id")+"&"+"room="+document.getElementById("room-number").innerHTML+"&pk="+$(this).attr("data-url")
        idup =$(this).attr("id");
        $.ajax({
            url:urlpoint,
            type:"GET",
            dataType:"json",
            beforeSend:function(){
                $("#CRUDroom .modal-content").html("");
                $("#CRUDroom").modal("show");  
            },
            success:function(data){
               
                $("#CRUDroom .modal-content").html(data.html_room_form);
                document.getElementsByClassName("js-update-form")[0].id=idup;
                document.getElementsByClassName("js-delete-room-form")[0].id =idup;
                

            }
        })
    };
    var saveDeleteAndUpdate = function(){
        console.log($(this))
        var form = $(this)
        $.ajax({
            url: form.attr("action"),
            type:form.attr("method"),
            data:form.serialize()+"&username="+$(this).attr("id")+"&pk="+$(this).attr("data-url"),
            dataType:'json',
            success:function(data){
                if (data.form_is_valid){
                    $(".content-card").html(data.html_room_list);
                    $("#CRUDroom").modal("hide");
                    document.getElementById("room-number").innerHTML=""
                    $(".generate-report").hide();
                }
                else{
                    $("#CRUDroom .modal-content").html(data.html_room_form);
                }
            }
        })
        return false;
    }
    //create the room
    // $('.js-create-room').click(loadForm);
    $("#myMain").on("click",".js-create-room",loadForm)
    $('#CRUDroom').on("submit",".js-create-room-form",saveForm);
    //update room
    // $('.js-update-room').click(loadForm);
    $(".dropdown-menu").on("click",".js-update-room",loadUpdateAndDelete);
    $("#CRUDroom").on('submit',".js-update-form",saveDeleteAndUpdate);
    //delete room
    // $('.js-delete-room').click(loadForm);
    $(".dropdown-menu").on("click",".js-delete-room",loadUpdateAndDelete)
    $('#CRUDroom').on('submit','.js-delete-room-form',saveDeleteAndUpdate);

})