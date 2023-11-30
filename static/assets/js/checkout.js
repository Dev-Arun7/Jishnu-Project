$(document).ready(function () {
    $('#rzp-button1').click(function (e) {
        e.preventDefault();
        var fname = $("[name='fname']").val();
        var mobile = $("[name='lname']").val();
        var address = $("[name='billing_address']").val();
        var token = $("[name= 'csrfmiddlewaretoken']").val();
        
        if (fname === '' || mobile === '' || address === ''){
            swal("Alert", "Please fill all fields!", "warning");
            return false;
        } else {
            $.ajax({
                type: "GET",
                url: "/proceed-to-pay",
                success: function(response){
                    var options = {
                        "key": "rzp_test_iUvmJdzDAlgu4E",
                        "amount": response.total_price * 100,
                        "currency": "INR",
                        "name": "DailyMart",
                        "description": "Thank You for Buying with us",
                        "image": "https://example.com/your_logo",
                        "handler": function (responseb){
                            var paymentId = responseb.razorpay_payment_id;
                            var paymentData = {
                                "payment_id" : paymentId,
                                csrfmiddlewaretoken: token
                            };
                            console.log(paymentId)

                            $.ajax({
                                type: "POST", // Change the type to POST
                                url: "/payment-completed/",
                                data: paymentData,
                                success: function(responsec){
                                    swal("congratulation!", "your payment sucessfull!", "success")
                                    .then((value) => {
                                    location.href = '/dashboard/'
                                    });
                                    
                                }
                            });
                        },
                        "prefill": {
                            "name": fname,
                            "contact": mobile
                        },
                        "notes": {
                            "address": "Razorpay Corporate Office"
                        },
                        "theme": {
                            "color": "#3399cc"
                        }
                    };
                    var rzp1 = new Razorpay(options);
                    rzp1.open();
                }
            });
        }
    });
});
