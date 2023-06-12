var stripe = Stripe('pk_test_51N7Hz4J3t7qnvvPUGytayKfUrhfJ6ddcoMEIJU8ptQcIBeKeIINjfE13tfItB8LAiDA0ULVkJjD6YMXgHNlF5el900IuA6hnZN');

var elem = document.getElementById('submit');
var clientsecret = elem.getAttribute('data-secret');

// Set up Stripe.js and Elements to use in checkout form
var elements = stripe.elements();
var style = {
  base: {
    color: "#000",
    lineHeight: '2.4',
    fontSize: '16px'
  }
};

var card = elements.create("card", { style: style });
card.mount("#card-element");

card.on('change', function(event) {
  var displayError = document.getElementById('card-errors')
  if (event.error) {
    displayError.textContent = event.error.message;
    $('#card-errors').addClass('alert alert-info');
  } else {
    displayError.textContent = '';
    $('#card-errors').removeClass('alert alert-info');
  }
});

var form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
  ev.preventDefault();

  var custName = document.getElementById("custName").value;
  var custAdd = document.getElementById("custAdd").value;
  var custAdd2 = document.getElementById("custAdd2").value;
  var postCode = document.getElementById("postCode").value;

  // Obtain CSRF token
  var csrftoken = getCookie('csrftoken');

  $.ajax({
    type: "POST",
    url: '/orders/add/',
    headers: {
      'X-CSRFToken': csrftoken
    },
    data: {
      order_key: clientsecret,
      csrfmiddlewaretoken: csrftoken,
      action: "post",
      full_name: custName,
      address1: custAdd,
      address2: custAdd2,
      post_code: postCode
    },

    success: function (json) {
      console.log(json.success);

      stripe.confirmCardPayment(clientsecret, {
        payment_method: {
          card: card,
          billing_details: {
            address: {
              line1: custAdd,
              line2: custAdd2
            },
            name: custName
          },
        }
      }).then(function(result) {
        if (result.error) {
          console.log('payment error');
          console.log(result.error.message);
        } else {
          if (result.paymentIntent.status === 'succeeded') {
            console.log('payment processed');
            updateBillingStatus(clientsecret);
            window.location.replace("http://127.0.0.1:8000/payment/orderplaced/");
          }
        }
      });

    },
    error: function (xhr, errmsg, err) {},
  });
});

// Function to update billing status
function updateBillingStatus(orderKey) {
  // Obtain CSRF token
  var csrftoken = getCookie('csrftoken');

  $.ajax({
    type: "POST",
    url: '/orders/payment_confirmation/',
    headers: {
      'X-CSRFToken': csrftoken
    },
    data: {
      order_key: orderKey,
      csrfmiddlewaretoken: csrftoken,
    },
    success: function (json) {
      console.log(json.success);
      // Handle success response as needed
    },
    error: function (xhr, errmsg, err) {},
  });
}

// Function to get CSRF token from cookie
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
