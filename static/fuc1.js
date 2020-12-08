$('.oprator').on('click', '.edit-btn', function () {
    nid = $(this).parent().parent().children('.nid').text();
    location.href = '/editbook/'+nid;
})


$('.oprator').on('click', '.delete-btn', function () {
    nid = $(this).parent().parent().children('.nid').text();
    location.href = '/deletebook/'+nid;
})