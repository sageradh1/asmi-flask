console.log('UPload js has been loaded')

var btnUpload = $("#upload_file"),
		btnOuter = $(".button_outer");
	btnUpload.on("change", function(e){
		var ext = btnUpload.val().split('.').pop().toLowerCase();
		if($.inArray(ext, ['mp4','avi','csv','jpg']) == -1) {
			$(".error_msg").text("Invalid File.");
		} else {
			$(".error_msg").text("");
			$(".loading_text").text("Loading...");
			btnOuter.addClass("file_uploading");
			setTimeout(function(){
				btnOuter.addClass("file_uploaded");
			},3000);
			var uploadedFile = URL.createObjectURL(e.target.files[0]);
			setTimeout(function(){
				// $("#uploaded_view").append('<img src="'+uploadedFile+'" />').addClass("show");
				$(".loading_text").text("");
				$(".success_msg").text("File loaded.");
				var x = $('<input type="submit" class="btn btn-danger" value="Submit" style="margin-left: 410px;width:150px;"/>');
                $(".btn-submit").append(x);				
			},3500);
			
		}
	});
	// $(".file_remove").on("click", function(e){
	// 	$("#uploaded_view").removeClass("show");
	// 	$("#uploaded_view").find("img").remove();
	// 	btnOuter.removeClass("file_uploading");
	// 	btnOuter.removeClass("file_uploaded");
	// });



