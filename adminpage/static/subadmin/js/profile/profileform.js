var endpoint;
$("#changepassword").click(function(){
    console.log($(this))
    endpoint='/subadmin/profile/api/';
    $.ajax({
        method:"GET",
        url:endpoint,
        beforeSend:function(){
            $("#profilepuser .modal-content").html("")
            $("#profilepuser").modal("show");
        },
        success:(data)=>{
            console.log(data)
            $("#profilepuser .modal-content").html(data.html_list)
            if (data.form_is_valid){
                $("#profilepuser").modal("hide");
            }
            else{
                $("#profilepuser").html(data.html_list);
            }
        }
    })
})