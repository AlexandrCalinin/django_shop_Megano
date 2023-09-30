console.log("файл работает")


function cart_add(product_id, product_name, image, product_count, amount, seller){
console.log('workdwasd')

var csrf = $('meta[name="csrf-token"]').attr('content');
    $.ajax({
    url: 'add',
    type: 'POST',
    headers: {"X-CSRFToken": csrf},
    data: {'product': product_id,
           'product_name': product_name,
           'image': image,
           'count': product_count,
           'amount': amount,
           'seller': seller},

    dataType: 'json',
    success: (data) => {
    $('.CartBlock-block').html(data.result)
    },
    error: (error) => {
    console.log(error)}
    });

};

function cart_edit(product_id, count, seller){

var csrf = $('meta[name="csrf-token"]').attr('content');
    $.ajax({
    url: 'cart/change',
    type: 'POST',
    headers: {"X-CSRFToken": csrf},
    data: {'product': product_id, 'count': count, 'seller': seller},
    dataType: 'json',
    success: (data) => {

    $('.CartBlock-block').html(data.cart)
    $('.Cart-product[id="' + product_id  + '"' ).children('.Cart-block.Cart-block_row').children('.Cart-block.Cart-block_price').html(data.count_change)
    $('.Cart-block.Cart-block_total').html(data.total_amount)
    },
    error: (error) => {
    console.log(error)}
    });

};

function product_delete(product_id){

var csrf = $('meta[name="csrf-token"]').attr('content');
    $.ajax({
    url: 'cart/delete',
    type: 'POST',
    headers: {"X-CSRFToken": csrf},
    data: {'product': product_id},
    dataType: 'json',
    success: (data) => {
    $('.CartBlock-block').html(data.cart)
    $('.Cart-block.Cart-block_total').html(data.total_amount)
    $('.Cart-product[id="' + product_id  + '"' ).first().remove()
    console.log($('.Cart-product[id="' + product_id  + '"' ).first())
    },
    error: (error) => {
    console.log(error)}
    });

};

$('.Card-hover').on('click', 'a[class="Card-btn"]', function(){
    var product_id = $(this).parents('.Card').attr('id')
    var product_count = 1
    var amount = $(this).attr('value')
    var seller = $(this).attr('id')
    var product_name = $(this).attr('name')
    var image = $(this).parents('.Card').children('.Card-picture').attr('name')

    cart_add(product_id, product_name, image, product_count, amount, seller)
})

$('.Amount').on('click', 'button[class="Amount-add"]', function(){

    var product_id = $(this).parents(".Cart-product").attr("id")
    var count = 1
    var seller = $(this).attr('name')

    cart_edit(product_id, count, seller)
})

$('.Amount').on('click', 'button[class="Amount-remove"]', function(){

    var product_id = $(this).parents(".Cart-product").attr("id")
    var count = -1
    var seller = $(this).parent('.Amount').children('.Amount-add').attr('name')

    cart_edit(product_id, count, seller)
})

$('.Cart-block.Cart-block_delete').on('click', 'a[class="Cart-delete"]', function(){

    var product_id = $(this).parents(".Cart-product").attr("id")

   product_delete(product_id)
})