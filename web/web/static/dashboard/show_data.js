function show_data(){
	$.ajax({
　　　　　　url: 'http://explorer.newtonproject.beta.diynova.com/dashboard',
　　　　　　type: 'GET',
　　　　　　success: function (data) {
			$('#transactions').html(data.total_transactions);
			$('#height').html(data.current_height);
			$('#tps').html(data.tps);
			$("#morris-area-chart").html("");
			show_chart(data.txs);
		}
	});

};

function show_chart(content) {
	var data_list = [];
	for (var k in content){
		var data_dict = {};
		b_time = format_time(parseInt(k + '000'));
		data_dict['time'] = b_time;
		data_dict['transactions'] = content[k];
		data_list.push(data_dict);
	};
    Morris.Area({
        element: 'morris-area-chart',
        data: data_list,
        xkey: 'time',
        ykeys: ['transactions'],
        labels: ['transactions'],
        pointSize: 2,
        hideHover: 'auto',
        resize: true
    });
};

function format_time(stamp){
	var time = new Date(stamp);
	var y = time.getFullYear();
	var m = time.getMonth() + 1;
	var d = time.getDate();
	var h = time.getHours();
	var mm = time.getMinutes();
	var s = time.getSeconds();
	var f_time = y+'-'+m+'-'+d+' '+h+':'+mm+':'+s;
	return f_time;
}