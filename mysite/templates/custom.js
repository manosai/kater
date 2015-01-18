function signup() {
	var first = $('.firstname').val();
	var last = $('.lastname').val();

	$.ajax({
		'async': false,
		'url': '/create_user',
		'type': 'GET',
		'data': {
			'first_name': first,
			'last_name' : last
		},
		'success': function(data) {
			alert("Success");
			return;
		}
	});
}
