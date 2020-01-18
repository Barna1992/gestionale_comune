$(function() {
    $('#id_expired_date').addClass('datepicker')
    $( ".datepicker" ).datepicker({
      changeMonth: true,
      changeYear: true,
      yearRange: "1900:2012",
      // You can put more options here.

    });
});