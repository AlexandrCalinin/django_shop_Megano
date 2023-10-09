(() => {
  $(document).ready(function() {
    var form = $('.comparison-add');
    console.log('принта', form);

    function compareUpdating(product_id) {
        var data = {};
        data.product_id = product_id;
        var csrf_token = $('#comparison-add [name="csrfmiddlewaretoken"]').val();
        data["csrfmiddlewaretoken"] = csrf_token;
        var url = form.attr("action");
        console.log('принт дата', data);
        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            cache: true,
            success: function (data) {
                console.log('OK');
                console.log(data.product_id);
            },
            error: function () {
                console.log("error")
            }
        })
    }

//    form.on('submit', function(e) {
//      e.preventDefault();
//      console.log('123');
//      var compare_btns = $('.compare_btn');
//      console.log("compare_btns", compare_btns)
//      $.each(compare_btns, function(k, v) {
//          console.log('v', v);
//          var product_id = v.data('product_id');
//          console.log('v', v.data());
//          compareUpdating(prod_id)
//      });
//    });
    $(".compare_btn").on("click", "button[class='compare_btn']", function() {

      var product_id = $(this)

      console.log('product_id', product_id);
      compareUpdating(prod_id)
    })

  });
})();
