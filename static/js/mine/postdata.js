function json2url(json){
	json.t=Math.random();

	var arr=[];
	for(var name in json){
		arr.push(name+'='+json[name]);
	}
	return arr.join('&');
}

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


function dailynum(id, data){

	document.getElementById(id).innerHTML=data;
}

function index_o(str){
	var gstr = str.split(',');
	var strdata = [];
	for (var i=0;i<gstr.length;i++){
		var str = gstr[i].split('=');
		var oSstr = {};
		oSstr.label = str[0];
		oSstr.value = str[1];
		strdata.push(oSstr);
	}
	var oStr = {};
	oStr.element = 'morris-chart-donut';
	oStr.data = strdata;
	oStr.formatter = function (y) { return y + "%" ;};
	Morris.Donut(oStr);
	/*
	Morris.Donut({
	  element: 'morris-chart-donut',
	  data: [
	    {label: "Referral", value: 42.7},
	    {label: "Direct", value: 8.3},
	    {label: "Social", value: 12.8},
	    //{label: "Organic", value: 36.2}
	  ],
	  formatter: function (y) { return y + "%" ;}
	});
	*/
}

function index_tb(kind, str){
//str = "1=RecordInfo=1.67%，5=EcGHistoryData=8.33%，6=DeviceLog=10.00% "
	var strdata =  str.split(',');
	var strtr = "";
	for (var m=0; m<strdata.length; m++){
		stritem = strdata[m].split('=');
		var strtd = "";
		for (var n=0; n<3; n++){
			strtd += "<td>"+stritem[n]+"</td>";
		}
		strtr += "<tr>"+strtd+"</tr>";
	}
	document.getElementById(kind).innerHTML=strtr;
}

function poline(str){
	var gstr = str.split('=');
	var localtime = gstr[0] * 1000;
	var num = gstr[1].split(',');
	var dic = "";
	var strdata = [];
	for (var i=0; i<24; i++){
		var oSstr = {};
		oSstr.h = localtime + i*3600000;
		oSstr.visits = num[i];
		strdata.push(oSstr);
	}
	var oStr = {};
	oStr.element = 'morris-chart-area';
	oStr.data = strdata;
	oStr.xkey = 'h';
	oStr.ykeys = ['visits'];
	oStr.labels = ['Visits'];
	oStr.smooth = true;
	Morris.Area(oStr);

}

function podata(purl, pdata, gid){
	ajax({
		url:purl,
		type:'post',
		data:{
			key:pdata,
		},
		success:function(gdata){
			if(gdata){
				gd = gdata.split(':');
				if (gd[0] == 'num') {
					dailynum(gid, gd[1]);
				}else if(gd[0] == 'line'){
					poline(gd[1]);
				}else if(gd[0] == 'index_o'){
					index_o(gd[1]);
				}else if(gd[0] == 'index_tb'){
					index_tb(gid, gd[1]);
				}
			}
		},
		error:function(){
			console.log("Get nums Err!");
		}
	});
}


podata('index', 'index_num1', 'totalnum');
podata('index', 'index_num2', 'ecgnum');
podata('index', 'index_num3', 'runnum');
podata('index', 'index_num4', 'sdknum');
podata('index', 'line', 'null');
podata('index', 'index_o', 'null');
podata('index', 'index_ecg', 'tb1');
podata('index', 'index_run', 'tb2');
//poline("1460476800=20,2,3,4,5,6,7,8,9,23,11,12,13,14,15,16,17,18");
//index_o("IOS9=42.7,Android4.0=36.2,Android5.0=18.5,Android6.0=0.3,Others=3.3");

