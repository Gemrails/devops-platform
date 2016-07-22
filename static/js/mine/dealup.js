function resault(num, msg){
	if (num == 1){
		document.getElementById('resault1').innerHTML="<h4 style='color:orangered;'>" + msg + "</h4>";
	}else if(num == 2 || num == 5){
		document.getElementById('resault1').innerHTML="<h4 style='color:green;'>" + msg + "</h4>";
	}else{
		document.getElementById('resault1').innerHTML="<h4 style='color:red;'>" + msg + "</h4>";
	}
}

function ajaxfile(podata, URL){
	$.ajax({
    	type: "POST",
    	url: URL,
    	dataType : "json",
    	processData: false,  // 注意：让jQuery不要处理数据
    	contentType: false,  // 注意：让jQuery不要设置contentType
    	data: podata
	}).success(function(gdata) {
		//console.log(gdata);
		if (gdata){
			pswitch(gdata);
		}
	}).fail(function(gdata){
		gdata = 4;
		msg = "Update unsuccess!";
		resault(upturn, msg);
		return 500;
	});
}


function pswitch(preturn){
	var msg = "";
	switch(preturn){
		case 1:
			msg = "Checkout success.Begin to send file...";
			resault(preturn, msg);
			ajaxfile(form_data, 'upfile');
			break;
		case 2:
			msg = "Receive sucess.Begin to update...";
			resault(preturn, msg);
			ajaxfile(form_data_up, 'upcomplete');
			break;
		case 5:
			msg = "Update completed.";
			resault(preturn, msg);
		case 8:
			msg = "Have no permission to update!";
			resault(preturn, msg);
			break;
		case 7:
			msg = "Receive file Error!";
			resault(preturn, msg);
		case 9:
			msg = "Update failed!!";
			resault(preturn, msg);
		case 500:
			msg = "Unknow Error!";
			resault(preturn, msg)
	}
}

function JudgeFrame(){
	var select1 = document.getElementById('select1').value;
	var filedata = document.getElementById('filepath').files[0];
	var info1 = document.getElementById('info1').value;
	var info2 = document.getElementById('info2').value;

	if(!select1){
		document.getElementById('selectp').innerHTML=" * 错误的项目选择";
		return
	}else if (!filedata || filedata.name.split('.')[1] != 'zip'){
		document.getElementById('filepathp').innerHTML=" * 错误的文件类型";
		return
	}else if(select1 != filedata.name.split('.')[0]){
		document.getElementById('filepathp').innerHTML=" * 选择的工程与压缩包不对应";
		return
	}else if (!info1){
		document.getElementById('info1p').innerHTML=" * 填写的更新信息不正确";
		return
	}else if (!info2){
		document.getElementById('info2').innerHTML=" * 填写的许可码不正确";
		return
	}else{
		//selectImage(filepath);
		var form_data = new FormData();
		form_data.append("project", select1);
		form_data.append("file", filedata);
		form_data.append("info1", info1);
		form_data.append("info2", info2);
		form_data.append("filename", filedata.name);
		form_data.append("extra", "other_info");

		var form_data_less = new FormData();
		form_data_less.append("info2", info2);

		var form_data_up = new FormData();
		form_data_up.append("pname",select1);
		//console.log(form_data);	
		var URL = 'up';
		$.ajax({
	    	type: "POST",
	    	url: URL,
	    	dataType : "json",
	    	processData: false,  // 注意：让jQuery不要处理数据
	    	contentType: false,  // 注意：让jQuery不要设置contentType
	    	data: form_data_less
		}).success(function(gdata) {
    		//console.log(gdata);
    		if (gdata){
    			var msg = "";
    			switch(gdata){
    				case 1:
    					msg = "Checkout success.Begin to send file...";
    					resault(gdata, msg);
    					$.ajax({
    						type: "POST",
    						url:'upfile',
    						dataType: "json",
    						processData: false,
    						contentType: false,
    						data: form_data
    					}).success(function(mdata){
    						if (mdata){
    							var msg = "";
    							switch(mdata){
    								case 2:
    									msg = "Receive sucess.Begin to update...";
    									resault(mdata, msg);
    									$.ajax({
    										type:"POST",
    										url:'upcomplete',
    										dataType:"json",
    										processData: false,
    										contentType: false,
    										data: form_data_up
    									}).success(function(upturn){
    										if(upturn){
    											var msg = "";
    											switch(upturn){
    												case 5:
    													msg = "Update completed.";
    													resault(upturn, msg);
    													break;
    												case 9:
    													msg = "Update failed!!";
    													resault(upturn, msg);
    													return;
    													break;
    											}
    										}
    									}).fail(function(upturn){
    										upturn = 4;
    										msg = "Update unsuccess!";
    										resault(upturn, msg);
    										return;
    									});
    									break;
				    				case 7:
				    					msg = "Receive file Error!";
				    					resault(mdata, msg);
				    					return;
					    				break;
    							}

    						}
    					}).fail(function(mdata){
							gdata = 4;
							msg = "Send timeout!";
							resault(mdata, msg);
							return;
						});
    					break;
    				case 8:
    					msg = "Have no permission to update!";
    					resault(gdata, msg);
    					break;
    			}
    		}
		}).fail(function(gdata) {
    		gdata = 4;
    		msg = "Send timeout!";
    		resault(gdata, msg)
    		return;
		});
	}
}

		





