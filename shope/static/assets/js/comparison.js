(() => {
  $(document).ready(function() {
    var form = $('.comparison-add');
    console.log('принта', form);

    function compareUpdating(product_id, url) {
      var data = {};
      data.product_id = product_id;
      var csrf_token = $('meta[name="csrf-token"]').attr('content');
      data["csrfmiddlewaretoken"] = csrf_token;
      console.log('принт url', url);
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

    form.on('submit', function(e) {
      e.preventDefault();
      console.log('123');
      var compare_btns = $('.compare_btn');
      console.log("compare_btns", compare_btns)
      $.each(compare_btns, function(k, v) {
        console.log('v', v);
        console.log('k', k);
        $(this).on('click', function(e) {
          e.preventDefault();
          var product_id = $(this).attr('data-product_id')
          var url = $(this).parents('.comparison-add').attr('action')
          console.log('product_id', product_id);
          compareUpdating(product_id, url)
        })
        console.log($(this).attr('data-product_id'));
//          v.addEventListener('click', onBtnClick);
//          v.addEventListener('click', function(event) {
//            event.preventDefault();
//            console.log('clicked');
//          });
//          compareUpdating(product_id)
      });
    });
  });
})();

