var endpoint;
function loadData(){
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
            $("#profilepuser .modal-content").html(data.html_list)
        }
    })
}
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
                $("#profilepuser").modal("hide");
            }
            else{
                console.log(data);
                $("#profilepuser .modal-content").html(data.html_list);
            }
        }
    });
    return false;
};


$("#changepassword").click(loadData);
$("#profilepuser").on("submit",".js-profile",saveForm)
