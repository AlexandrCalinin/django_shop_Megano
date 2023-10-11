(() => {
  $(document).ready(function() {
    var form = $('.comparison-add');

    function compareUpdating(product_id, url) {
      var data = {};
      data.product_id = product_id;
      var csrf_token = $('meta[name="csrf-token"]').attr('content');
      data["csrfmiddlewaretoken"] = csrf_token;
      $.ajax({
        url: url,
        type: 'POST',
        data: data,
        cache: true,
        success: function (data) {
          console.log('OK');
          alert(data.message)
        },
        error: function () {
          console.log("error")
          alert(data.message)
        }
      })
    }

    form.on('submit', function(e) {
      e.preventDefault();
      var compare_btns = $('.compare_btn');
      $.each(compare_btns, function(k, v) {
        $(this).on('click', function(e) {
          e.preventDefault();
          var product_id = $(this).attr('data-product_id')
          var url = $(this).parents('.comparison-add').attr('action')
          compareUpdating(product_id, url)
        })
      });
    });
  });
})();

