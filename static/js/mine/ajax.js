function ajax(json){
	json=json || {};
	if(!json.url)return;
	json.data=json.data || {};
	json.type=json.type || 'get';
	json.timeout=json.timeout || 5000;
	json.dataType=json.dataType || 'text';

	var timer=null;

	if(window.XMLHttpRequest){
		var oAjax=new XMLHttpRequest();
	}else{
		var oAjax=new ActiveXObject('Microsoft.XMLHTTP');
	}


	switch(json.type.toLowerCase()){
		case 'get':
			oAjax.open('GET',json.url+'?'+json2url(json.data),true);
			oAjax.send();
			break;
		case 'post':
			oAjax.open('POST',json.url,true);
			oAjax.setRequestHeader('Content-Type','application/x-www-form-urlencoded');
			oAjax.send(json2url(json.data));
			break;
	}

	//加载
	json.fnLoading && json.fnLoading();


	oAjax.onreadystatechange=function(){
		if(oAjax.readyState==4){
			json.complete && json.complete();
			clearTimeout(timer);
			if(oAjax.status>=200 && oAjax.status<300 || oAjax.status==304){
				if(json.dataType.toLowerCase()=='xml'){
					json.success && json.success(oAjax.responseXML);
				}else{
					json.success && json.success(oAjax.responseText);
				}
			}else{
				json.error && json.error(oAjax.status,oAjax.statusText);
			}
		}
	};

	timer=setTimeout(function(){
		json.complete && json.complete();
		json.error && json.error('网络超时');
		oAjax.onreadystatechange=null;
	},json.timeout);
}