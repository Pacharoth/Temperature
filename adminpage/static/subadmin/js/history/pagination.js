var search;
$('#search').keyup(function(){
    search='search/?page='+$(this).val();
    $.ajax({
        method:"GET",
        url:search,
        success:(data)=>{
            $("tbody").html(data.html_list);
            $('.pagination').html(data.html_list_pagination);
        }
    })
});
var searchdate;
$('#date_and_day').keyup(function(){
    console.log($(this).val());
    searchdate='/subadmin/profile/searchdate/?date_and_day='+$(this).val();
    $.ajax({
        method:'GET',
        url:searchdate,
        success:(data)=>{
            $("tbody").html(data.html_list);
            $('.pagination').html(data.html_list_pagination);
        }
    })
});
