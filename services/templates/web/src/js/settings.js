$(document).ready(function(){
  addNewUser();
});

function addNewUser() {
  $.ajax({
    type: "GET",
    url: apiURL + "/route/auth/addUserStoresList",
    contentType: "application/json; charset=utf-8",
    success: function(response) {
      var html = "";
      for (var i = 0; i < response.response.length; i++) {
        html += "<option value='" + response.response[i].store_id + "'>Store" + response.response[i].store_id + "</option>";
      }
      $('#js-addUser-stores').append(html);
    }
  });
}


$(document).delegate('#js-addUser-stores', 'change', function(ev) {
  ev.preventDefault();
  if ($('#js-addUser-stores option:selected').val() != 0) {
    $.ajax({
      type: "GET",
      url: apiURL + "/route/auth/addUser",
      data: {
        'store_id': $('#js-addUser-stores option:selected').val()
      },
      contentType: "application/json; charset=utf-8",
      success: function(response) {
        if (response.response.length > 0) {
          var html = '';
          for (var i = 0; i < response.response.length; i++) {
            html += "<option value='" + response.response[i].id + "'>" + response.response[i].name + "</option>";
          }
          $('#js-addUser-Designation').html(html);
          $('#js-addUser-Designation').prop("disabled", false);
          $('#js-addNewUser-submit').prop("disabled", false);
        } else {
          var html = '';
          new PNotify({
            title: 'Failed!',
            text: 'Sorry. There are no more roles available for the store',
            type: 'error',
            styling: 'fontawesome',
            hide: true,
            delay: 2000
          });
          $('#js-addUser-Designation').html('');
          $('#js-addUser-Designation').prop("disabled", true);
          $('#js-addNewUser-submit').prop("disabled", true);
        }
      }
    });
  } else {
    $('#js-addUser-Designation').html('');
    $('#js-addUser-Designation').prop("disabled", true);
  }
});

$('#js-addNewUser-submit').click(function(ev) {
  ev.preventDefault();
  if ($("#js-addUser-userId").val() && $("#js-addUser-userId").val() != '') {
    var userId = $("#js-addUser-userId").val();
  } else {
    var userId = '';
    if ($('#js-addUser-userId').parent().hasClass('has-error')) {} else {
      $('#js-addUser-userId').parent().addClass('has-error');
      $('#js-addUser-userId').parent().append('<p class="help-block">Please fill the userid.</p>');
    }
  }


  if ($("#js-addUser-inputName").val() && $("#js-addUser-inputName").val() != "") {
    var Name = $("#js-addUser-inputName").val();
  } else {
    var Name = '';
    if ($('#js-addUser-inputName').parent().hasClass('has-error')) {} else {
      $('#js-addUser-inputName').parent().addClass('has-error');
      $('#js-addUser-inputName').parent().append('<p class="help-block">Please fill the name.</p>');
    }
  }


  if ($("#js-addUser-E-mail").val() && $("#js-addUser-E-mail").val() != "") {
    var Email = $("#js-addUser-E-mail").val();
  } else {
    var Email = '';
    if ($('#js-addUser-E-mail').parent().hasClass('has-error')) {} else {
      $('#js-addUser-E-mail').parent().addClass('has-error');
      $('#js-addUser-E-mail').parent().append('<p class="help-block">Please fill the valid email.</p>');
    }
  }

  if ($("#js-addUser-Password").val() && $("#js-addUser-Password").val() != "") {
    var password = $.sha256($("#js-addUser-Password").val());
  } else {
    if ($('#js-addUser-Password').parent().hasClass('has-error')) {} else {
      $('#js-addUser-Password').parent().addClass('has-error');
      $('#js-addUser-Password').parent().append('<p class="help-block">Please fill the passsword.</p>');
    }
  }

  if ($("#js-addUser-Initials").val() && $("#js-addUser-Initials").val() != "") {
    var Initials = $("#js-addUser-Initials").val();
  } else {
    if ($('#js-addUser-Initials').parent().hasClass('has-error')) {} else {
      $('#js-addUser-Initials').parent().addClass('has-error');
      $('#js-addUser-Initials').parent().append('<p class="help-block">Please fill the initials.</p>');
    }
  }

  var Designation = $("#js-addUser-Designation option:selected").val();

  var Store = $('#js-addUser-stores option:selected').val();
  if (validateEmail($("#js-addUser-E-mail").val())) {
    if (userId && Name && Email && password && Initials) {
      $.ajax({
        type: "POST",
        url: apiURL + "/route/auth/addUser",
        data: JSON.stringify({
          "name": Name,
          "email": Email,
          "password": password,
          "initials": Initials,
          "user_id": userId,
          "store_id": Store,
          "role_id": Designation
        }),
        contentType: "application/json; charset=utf-8",
        success: function(response) {
          $('#js-signup-form').find("input[type=text], input[type=Name], input[type=password]").val("");
          $('#successmessage').show();
          $("#successmessage").fadeTo(2000, 500).slideUp(500, function() {
            $("#successmessage").hide();
          });
          $('#js-addNewUser-submit').prop("disabled", true);
          $('#js-addUser-Designation').html("");
          $('#js-addUser-Designation').prop("disabled", true);
          $('#js-signup-form').find('input[type=password],[type=Name],[type=email],[type=text]').val('')
          $('#js-addUser-stores').prop('selectedIndex', 0);
          $('#js-signup-form').find('p').remove();
          $('#js-signup-form').find('input').parent().removeClass('has-error');
          addNewUser();
        },
        error: function(xhr, ajaxOptions, thrownError) {
          new PNotify({
            title: 'SignUp Failed!',
            text: 'User has already existed for this store.',
            type: 'error',
            styling: 'fontawesome'
          });
          $('#js-addNewUser-submit').prop("disabled", true);
          $('#js-addUser-Designation').html("");
          $('#js-addUser-Designation').prop("disabled", true);
          $('#js-signup-form').find('input[type=password],[type=Name],[type=email],[type=text]').val('')
          $('#js-addUser-stores').prop('selectedIndex', 0);
          $('#js-signup-form').find('p').remove();
          $('#js-signup-form').find('input').parent().removeClass('has-error');
          addNewUser();
        }
      });
    }
  } else {
    if ($('#js-addUser-E-mail').parent().hasClass('has-error')) {} else {
      $('#js-addUser-E-mail').parent().addClass('has-error');
      $('#js-addUser-E-mail').parent().append('<p class="help-block">Please enter valid email.</p>');
    }
  }
});

$(document).delegate('#js-button-reset', 'click', function(ev) {
  $('#js-addUser-Designation').html("");
  $('#js-addUser-Designation').prop("disabled", true);
  $('#js-signup-form').find('p').remove();
  $('#js-signup-form').find('input').parent().removeClass('has-error');
});
