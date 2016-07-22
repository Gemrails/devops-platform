
function replacedom(id, num){
	//alert(num);
	if(document.getElementById(id)!=undefined){
		document.getElementById(id).innerHTML=num;
	}else{
		return;
	}
}

function getmaillog(){
	var mail = document.getElementById('email').value;
	formdata_mail = new FormData;
	formdata_mail.append('getmail', '1');
	formdata_mail.append('email', mail);
	$.ajax({
		type:"POST",
		url:'logmail',
		processData: false,
		contentType: false,
		data: formdata_mail
	}).success(function(getlog){
		if (getlog) {
			return;
		}
	}).fail(function(getlog){
		alert("Error!");
	});
}

function replacelog(id, context){
	var cont = [];
	var contmsg ='';
	cont = context.split('^.');
	for (var m=0; m<cont.length;m++){
		contmsg += '<nobr>' + cont[m] + '<nobr>' + '<br>';
	}
	contmsg = '<pre>' + contmsg + '</pre>';
	if(document.getElementById(id)!=undefined){
		document.getElementById(id).innerHTML=contmsg;
	}else{
		return;
	}
}

function logbtn(){
	var formdata_btn = new FormData;
	formdata_btn.append('btn', '1');
	$.ajax({
		type:"POST",
		url:'logbtn',
		processData: false,
		contentType: false,
		data: formdata_btn
	}).success(function(getlog){
		if (getlog) {
			if (getlog == 0) {
				replacedom('frame','==== 更新日志完成.====');
				alert('==== 更新日志完成.====');
			}else{
				replacedom('frame','==== 更新日志失败.====');
			}
		}
	}).fail(function(getlog){
		alert("Error!");
	});
}

function logget(id, key){
	var formdata_log = new FormData;
	formdata_log.append('gotlog', '1');
	formdata_log.append('kind',key);
	$.ajax({
		type:"POST",
		url:'logget',
		processData: false,
		contentType: false,
		data: formdata_log
	}).success(function(getlog){
		if (getlog) {
			replacelog(id, getlog)
		}
	}).fail(function(getlog){
		alert("Error!");
	});
}

function dealnum(gdata){
	var l1 = [];
	l1 = gdata.split(',')
	for (var i=0;i<l1.length;i++){
		var l2 = [];
		l2 = l1[i].split('-');
		replacedom(l2[0],l2[1]);
	}
}

var formdata = new FormData();
formdata.append('gotnum','1');
$.ajax({
    	type: "POST",
    	url:'logshow',
    	//dataType : "json",
    	processData: false,  // 注意：让jQuery不要处理数据
    	contentType: false,  // 注意：让jQuery不要设置contentType
    	data: formdata
	}).success(function(gdata){
		if(gdata){
			dealnum(gdata);
		}
	}).fail(function(gdata){
		alert(123131);
	});









