console.log("файл работает")


function cart_edit(url, product_id, product_count, amount, seller){

var csrf = $('meta[name="csrf-token"]').attr('content');
    $.ajax({
    url: url,
    type: 'POST',
    headers: {"X-CSRFToken": csrf},
    data: {'product': product_id, 'count': product_count, 'amount': amount, 'seller': seller},
    dataType: 'json',
    success: (data) => {
    console.log('send')
    $('.CartBlock-block').html(data.result)
    },
    error: (error) => {
    console.log(error)}
    });

};


//$('.ProductCard-cart').on('click', 'a[class="btn btn_primary"]', function (){
////cart_edit();
//
//
//});


$('.Card-hover').on('click', 'button[class="Send_data"]', function(){
var product_id = $(this).parents('.Card').attr('id')
var product_count = 1
var amount = $(this).attr('value')
var seller = $(this).attr('name')


cart_edit('/catalog/catalog/', product_id, product_count, amount, seller)
})