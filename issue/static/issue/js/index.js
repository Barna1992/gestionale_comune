$(document).ready( function() {
  $('#id_expired_date').addClass('datepicker');
  $( ".datepicker" ).datepicker({
    changeMonth: true,
    changeYear: true,
    format: 'dd/mm/yyyy'
    // You can put more options here.

  });
  $('input[type=checkbox]').click( (i) => {
      if ( $(i.currentTarget).prop('checked') ) {
          $(i.currentTarget).parent().removeClass('button-checkbox').addClass('button-checkbox-checked');
      }
      else {
          $(i.currentTarget).parent().removeClass('button-checkbox-checked').addClass('button-checkbox');
      }
  })
});
