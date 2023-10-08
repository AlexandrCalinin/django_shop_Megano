(() => {
  $(document).ready(function() {
    var form = $('#comparison-add');
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

    form.on('submit', function(e) {
      e.preventDefault();
      console.log('123');
      var compare_btn = $('#compare_btn');
      var product_id = compare_btn.data('product_id');
      compareUpdating(product_id)
    });

  });
})();
