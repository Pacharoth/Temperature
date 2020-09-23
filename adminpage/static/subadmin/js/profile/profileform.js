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
            $(".errorlist").hide()
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
                $("#profilepuser .modal-content").html(data.html_list);
                $('.errorlist').show();
            }
        }
    });
    return false;
};


// $("button .reveal_password1").click(reveal);
// $("button .reveal_password2").click(reveal1);

$("#changepassword").click(loadData);
$("#profilepuser").on("submit",".js-profile",saveForm)
