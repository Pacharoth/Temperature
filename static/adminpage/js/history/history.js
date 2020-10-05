var datetime ;
var user;
function search(){
    datetime =document.getElementById("formGroupExampleInput").value
    user = document.getElementById("user").value
    $.ajax({
        url:"/adminpage/search/?date_and_day="+datetime+"&user="+user,
        method:"GET",
        success:function(data){
            $("tbody").html(data.html_list)
            $(".js-pagination").html(data.html_pagination)
        }
    })
}
   