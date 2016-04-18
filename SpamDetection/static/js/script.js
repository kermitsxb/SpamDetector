$(document).ready(function () {
	// initialize with defaults
	$("#file-0a").fileinput();

	// with plugin options
	$("#file-0a").fileinput({'showUpload':false, 'previewFileType':'any'});

	/*$(function() {
		$('#dataForm').submit(function() {
			return validationEcran2();
		});
	});*/

	/*$("input[type='number']").change(function(){
		console.log("SISI");
		//console.log($(this).val());
		if($(this).val() < 0) {
			$(this).val(0);
		}
	});*/
});



function handleCheckbox(cb){
	var i = 0;
	if(cb.checked == true){
		$(':checkbox').each(function() {
			if (this.checked){
				i++;
			}
		});	

		if (i > 3){
			cb.checked = false;
		}
	}
}

function validationEcran2(){
	var chkChecked = [], 
	resultMesg = "", 
	resultToken = true;
	$(':checkbox').each(function() {
		if (this.checked){
			chkChecked.push(this);
		}
	});	

	if (chkChecked.length > 3){
		resultMesg = "Vous ne pouvez sélectionner que 3 colonnes."
		resultToken = false;
	}

	if (chkChecked.length < 2){
		resultMesg = "Veuillez sélectionner au moins 2 colonnes."
		resultToken = false;
	}

	if (resultMesg != ""){
		alert(resultMesg);	
	}
	
	return resultToken;
}
