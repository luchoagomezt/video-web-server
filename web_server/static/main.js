$(document).ready(function(){
				$('input[type="file"]').change(function(e) {
  					var i = $(this).prev('label').clone();
  					var file = e.target.files[0].name;
  					$(this).prev('label').text(file);
 				});
			});