$(function(){
    var button;
    function loadUser(){
        button = $(this).attr("data-url")
        $.ajax({
            url: button,
            method:"GET",
            beforeSend:function(){
                $('#CRUDroom .modal-content').html("");
                $("#CRUDroom").modal("show");
            },
            success:function(data){
                $("#CRUDroom .modal-content").html(data.html_form_list)
            }
        })
    }

    var saveUser = function(){
       var form = $(this)
        $.ajax({
            url:form.attr("action"),
            data:form.serialize(),
            type:form.attr("method"),
            dataType:"json",
            success:function(data){
                console.log(form.serialize())
                if (data.form_is_valid){
                    $("body").html(data.html_list)
                    $("#CRUDroom").modal("hide")
                    
                }else{
                    $('#CRUDroom .modal-content').html(data.html_form_list)
                }
            }
        });
        return false;
    };
    $('.js-edit-user').click(loadUser);
    $('#CRUDroom').on("submit",".js-change-user",saveUser);
    $('.js-delete-subadmin').click(loadUser);
    $("#CRUDroom").on("submit",".js-delete-user",saveUser);
})
    