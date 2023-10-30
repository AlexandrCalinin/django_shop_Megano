console.log("файл работает")


function cart_add(product_id, product_name, image, product_count, amount, seller){
// Функция отправляет запрос на добавление товара в корзину

var csrf = $('meta[name="csrf-token"]').attr('content');
    $.ajax({
    url: '/cart/add',
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
    Swal.fire({title: data.message, confirmButtonColor: '#0041c2',

})
    },
    error: (error) => {
    console.log(error)}
    });

};

function cart_edit(product_id, count, seller){
// Функция отправляет запрос на изменение кол-ва товаров в корзине

var csrf = $('meta[name="csrf-token"]').attr('content');
    $.ajax({
    url: '/cart/change',
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

    }
    });

};

function product_delete(product_id){
// Функция отправляет запрос на удаление товара из корзины

var csrf = $('meta[name="csrf-token"]').attr('content');
    $.ajax({
    url: '/cart/delete',
    type: 'POST',
    headers: {"X-CSRFToken": csrf},
    data: {'product': product_id},
    dataType: 'json',
    success: (data) => {
    $('.CartBlock-block').html(data.cart)
    $('.Cart-block.Cart-block_total').html(data.total_amount)
    $('.form.Cart').html(data.new_qs)
//    $('.Cart-product[id="' + product_id  + '"' ).remove()

    },
    error: (error) => {
    console.log(error)}
    });

};

$('.Card-hover').on('click', 'a[class="Card-btn cart-btn"]', function(){
   // Обработка нажатия на кнопку добавления товара в корзину на главной странице

    var product_id = $(this).parents('.Card').data('product')
    var product_count = 1
    var amount = $(this).data('value')
    var seller = $(this).data('seller')
    var product_name = $(this).data('name')
    var image = $(this).parents('.Card').children('form').children('.Card-picture').data('name')


    cart_add(product_id, product_name, image, product_count, amount, seller)
})

$('div[name="amount-cart"]').on('click', 'button[class="Amount-add"]', function(){
    // Обработка нажатия на кнопку добавления кол-ва товаров в корзине
    var count_product = $(this).parent('.Amount').children('.Amount-input.form-input').attr('value')
    $(this).parent('.Amount').children('.Amount-input.form-input').attr('value', parseInt(count_product) + 1)
    var count_product = $(this).parent('.Amount').children('.Amount-input.form-input').attr('value')

    var product_id = $(this).parents(".Cart-product").attr("id")
    var count = 1
    var seller = $(this).attr('name')

    cart_edit(product_id, count, seller)
})

$('div[name="amount-cart"]').on('click', 'button[class="Amount-remove"]', function(){
    // Обработка нажатия на кнопку уменьшения кол-ва товаров в корзине
    var count_product = $(this).parent('.Amount').children('.Amount-input.form-input').attr('value')
    $(this).parent('.Amount').children('.Amount-input.form-input').attr('value', parseInt(count_product) - 1)
    var count_product = $(this).parent('.Amount').children('.Amount-input.form-input').attr('value')
    var product_id = $(this).parents(".Cart-product").attr("id")
    var count = -1
    var seller = $(this).parent('.Amount').children('.Amount-add').attr('name')
    if(count_product == 0){
        product_delete(product_id)
    }
    else{
        cart_edit(product_id, count, seller)
    }
})

$('.Cart-block.Cart-block_delete').on('click', 'a[class="Cart-delete"]', function(){
    // Обработка нажатия на кнопку удаления товаров из корзину

    var product_id = $(this).parents(".Cart-product").attr("id")

   product_delete(product_id)
})

$('#1').on('click', 'a[class="btn btn_primary"]', function(){
   // Обработка нажатия на кнопку добавления товара в корзину на детальной странице продукта

    var product_id = $('.Product').attr('id')
    var product_count = $('.Amount-input.form-input').attr('value')
    var amount = $(this).data('value')
    var seller = $(this).data('seller')
    var product_name = $(this).data('name')
    var image = $('.ProductCard-pict').attr('href')
    if(product_count == 0){
        Swal.fire({title: 'Выберите кол-во товаров!', confirmButtonColor: '#0041c2'})
    }
    else{
        cart_add(product_id, product_name, image, product_count, amount, seller)
    }


})

$('div[name="add-product-to"]').on('click', 'a[class="btn btn_primary"]', function(){
   // Обработка нажатия на кнопку добавления товара в корзину на детальной странице продукта c продацами

    var product_id = $('.Product').attr('id')
    var product_count = $('.Amount-input.form-input').attr('value')
    var amount = $(this).data('value')
    var seller = $(this).data('seller')
    var product_name = $(this).data('name')
    var image = $('.ProductCard-pict').attr('href')


    cart_add(product_id, product_name, image, product_count, amount, seller)
})

$('.Amount').on('click', 'button[class="Amount-add"]', function(){

    var count_product = $(this).parent('.Amount').children('.Amount-input.form-input').attr('value')
    $(this).parent('.Amount').children('.Amount-input.form-input').attr('value', parseInt(count_product) + 1)
    var count_product = $(this).parent('.Amount').children('.Amount-input.form-input').attr('value')

})

$('.Amount').on('click', 'button[class="Amount-remove"]', function(){

    var count_product = $(this).parent('.Amount').children('.Amount-input.form-input').attr('value')
    $(this).parent('.Amount').children('.Amount-input.form-input').attr('value', parseInt(count_product) - 1)
    var count_product = $(this).parent('.Amount').children('.Amount-input.form-input').attr('value')


})


$('.ProductCard-cartElement').on('click', 'a[class="btn btn_primary"]', function(){
   // Обработка нажатия на кнопку добавления товара в корзину на странице сравнения

    var product_id = $(this).data('product')
    var product_count = 1
    var amount = $(this).data('value')
    var seller = $(this).data('seller')
    var product_name = $(this).data('name')
    var image = $(this).data('image')

    cart_add(product_id, product_name, image, product_count, amount, seller)
})