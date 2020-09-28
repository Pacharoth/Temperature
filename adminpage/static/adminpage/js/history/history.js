var datetime ;
function search(){
    datetime =document.getElementById("formGroupExampleInput").value
    $.ajax({
        url:"/adminpage/search/?date_and_day="+datetime,
        method:"GET",
        success:function(data){
            $("tbody").html(data.html_list)
            $(".js-pagination").html(data.html_pagination)
        }
    })
}   