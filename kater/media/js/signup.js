/* 
Orginal Page: http://thecodeplayer.com/walkthrough/jquery-multi-step-form-with-progress-bar 

*/
//jQuery time
var current_fs, next_fs, previous_fs; //fieldsets
var left, opacity, scale; //fieldset properties which we will animate
var animating; //flag to prevent quick multi-click glitches

$(".next").click(function(){
	if(animating) return false;
	animating = true;
	
	current_fs = $(this).parent();
	next_fs = $(this).parent().next();
	
	//activate next step on progressbar using the index of next_fs
	$("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");
	
	//show the next fieldset
	next_fs.show(); 
	//hide the current fieldset with style
	current_fs.animate({opacity: 0}, {
		step: function(now, mx) {
			//as the opacity of current_fs reduces to 0 - stored in "now"
			//1. scale current_fs down to 80%
			scale = 1 - (1 - now) * 0.2;
			//2. bring next_fs from the right(50%)
			left = (now * 50)+"%";
			//3. increase opacity of next_fs to 1 as it moves in
			opacity = 1 - now;
			current_fs.css({'transform': 'scale('+scale+')'});
			next_fs.css({'left': left, 'opacity': opacity});
		}, 
		duration: 800, 
		complete: function(){
			current_fs.hide();
			animating = false;
		}, 
		//this comes from the custom easing plugin
		easing: 'easeInOutBack'
	});
});

$(".previous").click(function(){
	if(animating) return false;
	animating = true;
	
	current_fs = $(this).parent();
	previous_fs = $(this).parent().prev();
	
	//de-activate current step on progressbar
	$("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");
	
	//show the previous fieldset
	previous_fs.show(); 
	//hide the current fieldset with style
	current_fs.animate({opacity: 0}, {
		step: function(now, mx) {
			//as the opacity of current_fs reduces to 0 - stored in "now"
			//1. scale previous_fs from 80% to 100%
			scale = 0.8 + (1 - now) * 0.2;
			//2. take current_fs to the right(50%) - from 0%
			left = ((1-now) * 50)+"%";
			//3. increase opacity of previous_fs to 1 as it moves in
			opacity = 1 - now;
			current_fs.css({'left': left});
			previous_fs.css({'transform': 'scale('+scale+')', 'opacity': opacity});
		}, 
		duration: 800, 
		complete: function(){
			current_fs.hide();
			animating = false;
		}, 
		//this comes from the custom easing plugin
		easing: 'easeInOutBack'
	});
});

$(".submit").click(function(){
	var email = $("input[name='email']").val();
	var pass = $("input[name='pass']").val();
	var cpass = $("input[name='cpass']").val();
	var fname = $("input[name='fname']").val();
	var lname = $("input[name='lname']").val();
	var address = $("input[name='address']").val();
	var city = $("input[name='city']").val();
	var state = $("select[name='state']").val();
	var phone = $("input[name='phone']").val();

	var budget = $("input[name='budget']").val();
	var allergies = $("input[name='allergies']").val();

	var meals = "";
	var mealsArr = $("input[type='checkbox']");
	for (i=0; i<21; i++) {
		var meal = mealsArr[i];
		if (meal.checked) {
			meals += "1";
		}
		else {
			meals += "0";
		}
	}

	var meats = "";
	if ($("#chicken")[0].checked) {
		meats +="Chicken,"
	}
	if ($("#pork")[0].checked) {
		meats +="Pork,"
	}
	if ($("#beef")[0].checked) {
		meats +="Beef,"
	}
	if ($("#seafood")[0].checked) {
		meats +="Seafood,"
	}

	var cuisines = "";
	var cuisinesChecks = $(".cuisineCheck");
	var cuisineLabels = $(".cuisineLabel");
	alert("hey");
	for (i=0; i<16; i++) {

		if (cuisinesChecks[i].checked) {
			cuisines += cuisineLabels[i].innerText + ",";
		}
	}

	var healthy;
	if ($("#healthy")[0].checked) {
		healthy = true;
	}
	else {
		healthy = false;
	}

	var postRequest = {'email': email, 'pass': pass, 'fname': fname, 'lname': lname, 'address': address, 'city': city, 'state': state, 'phone': phone, 'budget': budget, 'allergies': allergies, 'meals': meals, 'meats': meats, 'cuisines': cuisines, 'healthy': healthy};

	$.ajax({
		'async': false,
		'url': '/create_user',
		'type': 'POST',
		'data': {
			'data': postRequest
		},
		'success': function(data) {
			alert("Success");
			return false;
		},
		'error': function(data) {
			alert("Failure");
			return false;
		}
	});
	return false;

})
