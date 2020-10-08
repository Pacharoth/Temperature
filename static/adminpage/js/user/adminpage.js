var userID;
function searchItem(){
    userID = document.getElementById("search").value
    $.ajax({
        url:'/adminpage/searchcard/?user='+userID,
        method:"GET",
        success:function(data){
            $("html").html(data.html_list);
        }
    })
}
var otheruser;
function searchUser(){
    otheruser = document.getElementById("otheruser").value
    $.ajax({
        url:'/adminpage/searchcard/?user='+otheruser,
        method:"GET",
        success:function(data){
            $("html").html(data.html_list);
        }
    })
}
