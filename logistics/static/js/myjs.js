$(document).ready(function(){
  
    $(".datetimeinput").datepicker({changeYear: false,changeMonth: true, dateFormat: 'yy-mm-dd'});
   

    $('.table').paging({limit:3});
  });
