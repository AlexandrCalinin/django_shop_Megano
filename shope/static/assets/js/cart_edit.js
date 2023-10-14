console.log("файл работает")


function cart_add(product_id, product_name, image, product_count, amount, seller){
// Функция отправляет запрос на добавление товара в корзину

var csrf = $('meta[name="csrf-token"]').attr('content');
    $.ajax({
    url: '/cart/cart/add',
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
    Swal.fire({title: 'Товар добавлен в корзину!', confirmButtonColor: '#0041c2',

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
// Функция отправляет запрос на удаление товара из корзины

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
    $('.Cart-product[id="' + product_id  + '"' ).remove()
    console.log($('.Cart-product[id="' + product_id  + '"' ).first())
    },
    error: (error) => {
    console.log(error)}
    });

};

$('.Card-hover').on('click', 'a[class="Card-btn"]', function(){
   // Обработка нажатия на кнопку добавления товара в корзину в каталоге

    var product_id = $(this).parents('.Card').attr('id')
    var product_count = 1
    var amount = $(this).data('value')
    var seller = $(this).attr('id')
    var product_name = $(this).attr('name')
    var image = $(this).parents('.Card').children('.Card-picture').attr('name')

    cart_add(product_id, product_name, image, product_count, amount, seller)
})

$('#amount').on('click', 'button[class="Amount-add"]', function(){
    // Обработка нажатия на кнопку добавления кол-ва товаров в корзине
    var count_product = $(this).parent('.Amount').children('.Amount-input.form-input').attr('value')
    $(this).parent('.Amount').children('.Amount-input.form-input').attr('value', parseInt(count_product) + 1)
    var count_product = $(this).parent('.Amount').children('.Amount-input.form-input').attr('value')

    var product_id = $(this).parents(".Cart-product").attr("id")
    var count = 1
    var seller = $(this).attr('name')
    console.log(count_product)

    cart_edit(product_id, count, seller)
})

$('#amount').on('click', 'button[class="Amount-remove"]', function(){
    // Обработка нажатия на кнопку уменьшения кол-ва товаров в корзине
    var count_product = $(this).parent('.Amount').children('.Amount-input.form-input').attr('value')
    $(this).parent('.Amount').children('.Amount-input.form-input').attr('value', parseInt(count_product) - 1)
    var count_product = $(this).parent('.Amount').children('.Amount-input.form-input').attr('value')
console.log(count_product)
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
    var seller = $(this).attr('id')
    var product_name = $(this).attr('name')
    var image = $('.ProductCard-pict').attr('href')
    console.log('product', product_id)
    console.log('count', product_count)
    console.log('amount', amount)
    console.log('seller', seller)
    console.log('name', product_name)
    console.log('image', image)

    cart_add(product_id, product_name, image, product_count, amount, seller)
})

$('div[name="add-product-to"]').on('click', 'a[class="btn btn_primary"]', function(){
   // Обработка нажатия на кнопку добавления товара в корзину на детальной странице продукта

    var product_id = $('.Product').attr('id')
    var product_count = $('.Amount-input.form-input').attr('value')
    var amount = $(this).data('value')
    var seller = $(this).data('seller')
    var product_name = $(this).data('name')
    var image = $('.ProductCard-pict').attr('href')
    console.log('product', product_id)
    console.log('count', product_count)
    console.log('amount', amount)
    console.log('seller', seller)
    console.log('name', product_name)
    console.log('image', image)

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