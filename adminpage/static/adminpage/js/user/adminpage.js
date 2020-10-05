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
