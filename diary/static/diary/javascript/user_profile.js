

$(document).ready(function(){
    console.log('my jquery file');
    $('.modal').modal();
	$('select').material_select();
	$('.datepicker').pickadate({
    selectMonths: true, 
    selectYears: 60 
  	});
});


  