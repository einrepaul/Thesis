(function($) {

	"use strict";


})(jQuery);

var form_fields = document.getElementsByTagName('input')
form_fields[1].placeholder='First Name';
form_fields[2].placeholder='Last Name';
form_fields[3].placeholder='Email Address';
form_fields[4].placeholder='Password';
form_fields[5].placeholder='Confirm Password 2';

for (var field in form_fields){
	form_fields[field].className += 'form-control'
}