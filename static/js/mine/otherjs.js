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

function dealwithjson(json){



}

function dailynum(id, data){

	document.getElementById(id).innerHTML=data;
}

function poline(str){

	num = str.split(',');
	var strdata = [];
	var dic = "";
	for (var i = 0; i<23; i++){
		dic = "{d:'"+i+"',visits:"+num[i]+'}';
		strdata.push(dic);
	}
	alert(strdata);
	oStr = {};
	oStr.element = 'morris-chart-area';
	oStr.data = strdata;
	oStr.xkey = 'h';
	oStr.ykeys = ['visits'];
	oStr.labels = ['Visits'];
	oStr.smooth = false;
	console.log(oStr.data);

	oPer = {
	  	element: 'morris-chart-area',
	  data: [
		{ d: '2012-10-01', visits: 802 },
		{ d: '2012-10-02', visits: 783 },
		{ d: '2012-10-03', visits:  820 },
		{ d: '2012-10-04', visits: 839 },
		{ d: '2012-10-05', visits: 792 },
		{ d: '2012-10-06', visits: 859 },
		{ d: '2012-10-07', visits: 790 },
		{ d: '2012-10-08', visits: 1680 },
		{ d: '2012-10-09', visits: 1592 },
		{ d: '2012-10-10', visits: 1420 },
		{ d: '2012-10-11', visits: 882 },
		{ d: '2012-10-12', visits: 889 },
		{ d: '2012-10-13', visits: 819 },
		{ d: '2012-10-14', visits: 849 },
		{ d: '2012-10-15', visits: 870 },
		{ d: '2012-10-16', visits: 1063 },
		{ d: '2012-10-17', visits: 1192 },
		{ d: '2012-10-18', visits: 1224 },
		{ d: '2012-10-19', visits: 1329 },
		{ d: '2012-10-20', visits: 1329 },
		{ d: '2012-10-21', visits: 1239 },
		{ d: '2012-10-22', visits: 1190 },
		{ d: '2012-10-23', visits: 1312 },
		{ d: '2012-10-24', visits: 1293 },
		{ d: '2012-10-25', visits: 1283 },
		{ d: '2012-10-26', visits: 1248 },
		{ d: '2012-10-27', visits: 1323 },
		{ d: '2012-10-28', visits: 1390 },
		{ d: '2012-10-29', visits: 1420 },
		{ d: '2012-10-30', visits: 1529 },
		{ d: '2012-10-31', visits: 1892 },
	  ],

		xkey: 'h',
		ykeys: ['visits'],
		labels: ['Visits'],
	  	// Disables line smoothing
	  	smooth: false,
	};
	console.log(oPer);
	Morris.Area(oPer);
	/*Morris.Area({
	  	element: 'morris-chart-area',
	 	data: data,



	  data: [
		{ d: '2012-10-01', visits: 802 },
		{ d: '2012-10-02', visits: 783 },
		{ d: '2012-10-03', visits:  820 },
		{ d: '2012-10-04', visits: 839 },
		{ d: '2012-10-05', visits: 792 },
		{ d: '2012-10-06', visits: 859 },
		{ d: '2012-10-07', visits: 790 },
		{ d: '2012-10-08', visits: 1680 },
		{ d: '2012-10-09', visits: 1592 },
		{ d: '2012-10-10', visits: 1420 },
		{ d: '2012-10-11', visits: 882 },
		{ d: '2012-10-12', visits: 889 },
		{ d: '2012-10-13', visits: 819 },
		{ d: '2012-10-14', visits: 849 },
		{ d: '2012-10-15', visits: 870 },
		{ d: '2012-10-16', visits: 1063 },
		{ d: '2012-10-17', visits: 1192 },
		{ d: '2012-10-18', visits: 1224 },
		{ d: '2012-10-19', visits: 1329 },
		{ d: '2012-10-20', visits: 1329 },
		{ d: '2012-10-21', visits: 1239 },
		{ d: '2012-10-22', visits: 1190 },
		{ d: '2012-10-23', visits: 1312 },
		{ d: '2012-10-24', visits: 1293 },
		{ d: '2012-10-25', visits: 1283 },
		{ d: '2012-10-26', visits: 1248 },
		{ d: '2012-10-27', visits: 1323 },
		{ d: '2012-10-28', visits: 1390 },
		{ d: '2012-10-29', visits: 1420 },
		{ d: '2012-10-30', visits: 1529 },
		{ d: '2012-10-31', visits: 1892 },
	  ],

		xkey: 'h',
		ykeys: ['visits'],
		labels: ['Visits'],
	  	// Disables line smoothing
	  	smooth: false,
	});*/
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
				}
			}
		},
		error:function(){
			alert("Get nums Err!");
		}
	});
}


function index_o(){
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
}

function newpoline(){
	Morris.Area({
	  	element: 'morris-chart-area',
	  data: [
		{ d: '2012-10-01', visits: 802 },
		{ d: '2012-10-02', visits: 783 },
		{ d: '2012-10-03', visits:  820 },
		{ d: '2012-10-04', visits: 839 },
		{ d: '2012-10-05', visits: 792 },
		{ d: '2012-10-06', visits: 859 },
		{ d: '2012-10-07', visits: 790 },
		{ d: '2012-10-08', visits: 1680 },
		{ d: '2012-10-09', visits: 1592 },
		{ d: '2012-10-10', visits: 1420 },
		{ d: '2012-10-11', visits: 882 },
		{ d: '2012-10-12', visits: 889 },
		{ d: '2012-10-13', visits: 819 },
		{ d: '2012-10-14', visits: 849 },
		{ d: '2012-10-15', visits: 870 },
		{ d: '2012-10-16', visits: 1063 },
		{ d: '2012-10-17', visits: 1192 },
		{ d: '2012-10-18', visits: 1224 },
		{ d: '2012-10-19', visits: 1329 },
		{ d: '2012-10-20', visits: 1329 },
		{ d: '2012-10-21', visits: 1239 },
		{ d: '2012-10-22', visits: 1190 },
		{ d: '2012-10-23', visits: 1312 },
		{ d: '2012-10-24', visits: 1293 },
		{ d: '2012-10-25', visits: 1283 },
		{ d: '2012-10-26', visits: 1248 },
		{ d: '2012-10-27', visits: 1323 },
		{ d: '2012-10-28', visits: 1390 },
		{ d: '2012-10-29', visits: 1420 },
		{ d: '2012-10-30', visits: 1529 },
		{ d: '2012-10-31', visits: 1892 },
	  ],

		xkey: 'h',
		ykeys: ['visits'],
		labels: ['Visits'],
	  	// Disables line smoothing
	  	smooth: false,
	});
}

//podata('index', 'index_num1', 'totalnum');
//podata('index', 'index_num2', 'ecgnum');
//podata('index', 'index_num3', 'runnum');
//podata('index', 'index_num4', 'sdknum');
//poline("1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24");
//newpindex_o;
//podata('index', 'index_line', 'null');
// First Chart Example - Area Line Chart


Morris.Area({
	  	element: 'morris-chart-area',
	  data: [
		{ d: '2012-10-01', visits: 802 },
		{ d: '2012-10-02', visits: 783 },
		{ d: '2012-10-03', visits:  820 },
		{ d: '2012-10-04', visits: 839 },
		{ d: '2012-10-05', visits: 792 },
		{ d: '2012-10-06', visits: 859 },
		{ d: '2012-10-07', visits: 790 },
		{ d: '2012-10-08', visits: 1680 },
		{ d: '2012-10-09', visits: 1592 },
		{ d: '2012-10-10', visits: 1420 },
		{ d: '2012-10-11', visits: 882 },
		{ d: '2012-10-12', visits: 889 },
		{ d: '2012-10-13', visits: 819 },
		{ d: '2012-10-14', visits: 849 },
		{ d: '2012-10-15', visits: 870 },
		{ d: '2012-10-16', visits: 1063 },
		{ d: '2012-10-17', visits: 1192 },
		{ d: '2012-10-18', visits: 1224 },
		{ d: '2012-10-19', visits: 1329 },
		{ d: '2012-10-20', visits: 1329 },
		{ d: '2012-10-21', visits: 1239 },
		{ d: '2012-10-22', visits: 1190 },
		{ d: '2012-10-23', visits: 1312 },
		{ d: '2012-10-24', visits: 1293 },
		{ d: '2012-10-25', visits: 1283 },
		{ d: '2012-10-26', visits: 1248 },
		{ d: '2012-10-27', visits: 1323 },
		{ d: '2012-10-28', visits: 1390 },
		{ d: '2012-10-29', visits: 1420 },
		{ d: '2012-10-30', visits: 1529 },
		{ d: '2012-10-31', visits: 1892 },
	  ],

		xkey: 'h',
		ykeys: ['visits'],
		labels: ['Visits'],
	  	// Disables line smoothing
	  	smooth: false,
	});




Morris.Line({
  // ID of the element in which to draw the chart.
  element: 'morris-chart-line',
  // Chart data records -- each entry in this array corresponds to a point on
  // the chart.
  data: [
	{ d: '2012-10-01', visits: 802 },
	{ d: '2012-10-02', visits: 783 },
	{ d: '2012-10-03', visits:  820 },
	{ d: '2012-10-04', visits: 839 },
	{ d: '2012-10-05', visits: 792 },
	{ d: '2014-10-06', visits: 859 },
	{ d: '2012-10-07', visits: 790 },
	{ d: '2012-10-08', visits: 1680 },
	{ d: '2012-10-09', visits: 1592 },
	{ d: '2012-10-10', visits: 1420 },
	{ d: '2012-10-11', visits: 882 },
	{ d: '2012-10-12', visits: 889 },
	{ d: '2012-10-13', visits: 819 },
	{ d: '2012-10-14', visits: 849 },
	{ d: '2012-10-15', visits: 870 },
	{ d: '2012-10-16', visits: 1063 },
	{ d: '2012-10-17', visits: 1192 },
	{ d: '2012-10-18', visits: 1224 },
	{ d: '2012-10-19', visits: 1329 },
	{ d: '2012-10-20', visits: 1329 },
	{ d: '2012-10-21', visits: 1239 },
	{ d: '2012-10-22', visits: 1190 },
	{ d: '2012-10-23', visits: 1312 },
	{ d: '2012-10-24', visits: 1293 },
	{ d: '2012-10-25', visits: 1283 },
	{ d: '2012-10-26', visits: 1248 },
	{ d: '2012-10-27', visits: 1323 },
	{ d: '2012-10-28', visits: 1390 },
	{ d: '2012-10-29', visits: 1420 },
	{ d: '2012-10-30', visits: 1529 },
	{ d: '2012-10-31', visits: 1892 },
  ],
  // The name of the data record attribute that contains x-visitss.
  xkey: 'd',
  // A list of names of data record attributes that contain y-visitss.
  ykeys: ['visits'],
  // Labels for the ykeys -- will be displayed when you hover over the
  // chart.
  labels: ['Visits'],
  // Disables line smoothing
  smooth: false,
});

Morris.Bar ({
  element: 'morris-chart-bar',
  data: [
	{device: 'iPhone', geekbench: 136},
	{device: 'iPhone 3G', geekbench: 137},
	{device: 'iPhone 3GS', geekbench: 275},
	{device: 'iPhone 4', geekbench: 380},
	{device: 'iPhone 4S', geekbench: 655},
	{device: 'iPhone 5', geekbench: 1571}
  ],
  xkey: 'device',
  ykeys: ['geekbench'],
  labels: ['Geekbench'],
  barRatio: 0.4,
  xLabelAngle: 35,
  hideHover: 'auto'
});

/*
var URL = 'tables';
ajax({
	url:URL,
	type:'post',
	data:{
	    date:"20160320",
	    },
	success:function(data){
	    if(data){
	        console.log(data);
	    }else{
	        alert("NO!");
	    }
	},
	error:function(){
	    alert(arguments[1]);
	}

});


/*
var oChannelList = document.getElementById('channellist');
    var oNavList = document.getElementById('navlist');
    var aNavLi = oNavList.children;


    oChannelList.innerHTML = '';
    var oFragment = document.createDocumentFragment();
    for(var i=0,len=json.data.length; i<len; i++){
        var oLi = document.createElement('li');  //tr
        oLi.className = 'fl';
        oLi.innerHTML = '<a href="javascript:;">'+json.data[i].zone_name+'</a><input type="hidden" value="'+json.data[i].zonid+'"/>';

        oFragment.appendChild(oLi);

    }

    oChannelList.appendChild(oFragment);
*/