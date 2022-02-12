
$(document).ready(function(){

$(document).on('click','.increment-btn', function(e){
// $('.increment-btn').click(function(e){
    e.preventDefault();

    var inc_value = $(this).closest('.product_data').find('.qty-input').val();
    var value = parseInt(inc_value, 10);
    value = isNaN(value) ? 0 : value;
    if(value < 10)
    {
        value++;
        $(this).closest('.product_data').find('.qty-input').val(value);
    }
});

$(document).on('click','.decrement-btn', function(e){
// $('.decrement-btn').click(function(e){
    e.preventDefault();

    var dec_value = $(this).closest('.product_data').find('.qty-input').val();
    var value = parseInt(dec_value, 10);
    value = isNaN(value) ? 0 : value;
    if(value > 1)
    {
        value--;
        $(this).closest('.product_data').find('.qty-input').val(value);
    }
});
$('.addToCartBtn').click(function(e){
    e.preventDefault();

    var product_id = $(this).closest('.product_data').find('.prod_id').val(); 
    var product_qty = $(this).closest('.product_data').find('.qty-input').val();
    var token = $('input[name=csrfmiddlewaretoken]').val();
    $.ajax({
        method: "POST",
        url: "{% url 'add_To_Cart' %}",
        data: {
        'product_id':product_id,
        'product_qty':product_qty,
        csrfmiddlewaretoken: token
        },
        success: function (response){
        console.log(response)
        $('#loa').load(location.href + ' #loa');
        // alerty.success(response.status)
        }  
    });
});

$(document).on('click','.changeQuantity', function(e){
// $('.changeQuantity').click(function(e){
    e.preventDefault();

    var product_id = $(this).closest('.product_data').find('.prod_id').val(); 
    var product_qty = $(this).closest('.product_data').find('.qty-input').val();
    var token = $('input[name=csrfmiddlewaretoken]').val();
    $.ajax({
        method: "POST",
        url: "{% url 'update_cart' %}",
        data: {
        'product_id':product_id,
        'product_qty':product_qty,
        csrfmiddlewaretoken: token
        },
        success: function (response){
        console.log(response)
        $('.changeamount').load(location.href + ' .changeamount');
        $('.changevalue').load(location.href + ' .changevalue');
        $('.changetotal').load(location.href + ' .changetotal');
        $('.changetax').load(location.href + ' .changetax');
        $('.am').load(location.href + ' .am');
        
        // alerty.success(response.status)
        }  
    });
});

$(document).on('click','.deleteCartItem', function(e){
// $('.deleteCartItem').click(function(e){
    e.preventDefault();

    var product_id = $(this).closest('.product_data').find('.prod_id').val(); 
    var token = $('input[name=csrfmiddlewaretoken]').val();

    $.ajax({
        method: "POST",
        url: "delete_cart_item",
        data:{
        'product_id':product_id,
        csrfmiddlewaretoken: token
        },
        success:function(response){
        console.log(response)
        // $('.cartdata').load(location.href + " .cartdata");
        $('#loa').load(location.href + ' #loa');
        }
    });
});

});
