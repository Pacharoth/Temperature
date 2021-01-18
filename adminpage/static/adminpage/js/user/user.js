$(function(){
    function searchUser(){
        $.ajax({
            url:'/adminpage/searchuser/user/?username='+$("#searchUser").val(),
            type:"GET",
            dataType:"json",
            success:function(data){
                $('.js-change-list').html(data.html_list)
            }

        })
    }
    function searchUser1(){
        $.ajax({
            url:'/adminpage/searchuser/user/?username='+$("#searchUser1").val(),
            type:"GET",
            dataType:"json",
            success:function(data){
                $('.js-change-list').html(data.html_list)
            }

        })
    }
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
            type:form.attr("method"),
            data:form.serialize(),
            dataType:"json",
            success:function(data){
                if (data.form_is_valid){
                    $(".js-change-list").html(data.html_list)
                    $("#CRUDroom").modal("hide")
                    
                }else{
                    $('#CRUDroom .modal-content').html(data.html_form_list)
                }
            }
        });
        return false;
    };
    var saveDelete = function(){
        var form = $(this)
         $.ajax({
             url:form.attr("action"),
             data:form.serialize()+form.attr("id"),
             type:form.attr("method"),
             dataType:"json",
             success:function(data){
                 if (data.form_is_valid){

                     $(".js-change-list").html(data.html_list)
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
    $("#CRUDroom").on("submit",".js-delete-user",saveDelete);
    $("#js-search").click(searchUser);
    $("#jssearch").click(searchUser1);

})
    