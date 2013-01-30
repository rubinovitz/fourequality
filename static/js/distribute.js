// make sure form is submitted correctly
// control the addition of payment schemes
var MainView = Backbone.View.extend({

	el: 'body',


	events: {'click #submit-premiere': "submitForm"},

		initialize: function(){
		console.log('view intialized');
	},

	submitForm: function(){
		var formData = $('#project-desc').serialize();
		console.log(formData);
		$.ajax({
						url:'/premieres/apply/?'+formData,
						type:'POST',
						success: function(){
							console.log('form submitted!');
						}
			});
	}
});

$(document).ready(function() {
	var mainView = new MainView;
});
