$(document).ready(function(){

$('#panel').load('content/dashboard_default.html');
    
$('ul#nav li a').click(function(){        
        var page = $(this).attr('href');
        $('#panel').load('content/'+ page +'.html');
        return false;
    });
    
      
});


alert('i am here');



    

   

