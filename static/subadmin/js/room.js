$(function(){


    // function load modal form
    var loadForm = function(){
        var btn = $(this);
        
        $.ajax({
            url:btn.attr("data-url"),
            type:'get',
            dataType:'json',
            beforeSend:function(){
                $("#CRUDroom .modal-content").html("");
                $("#CRUDroom").modal("show");  
            },
            success:function(data){
                $("#CRUDroom .modal-content").html(data.html_room_form);
               
            }
        });
    };

    //save data and return the list of room
    var saveForm = function(){
        var form = $(this)
        console.log(form)
        $.ajax({
            url:form.attr("action"),
            data:form.serialize(),
            type:form.attr("method"),
            dataType:'json',
            success:function(data){
               
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
    $("#myModal").on("click",".js-create-room",loadForm)
    $('#CRUDroom').on("submit",".js-create-room-form",saveForm);

    //update room
    // $('.js-update-room').click(loadForm);
    $("#myModal").on("click",".js-update-room",loadForm)

    $('#CRUDroom').on("submit",'.js-update-room-form',saveForm);

    //delete room
    // $('.js-delete-room').click(loadForm);
    $("#myModal").on("click",".js-delete-room",loadForm)
    $('#CRUDroom').on('submit','.js-delete-room-form',saveForm);

})