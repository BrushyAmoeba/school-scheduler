var app = angular.module('scheduler', ['ui.directives']);

app.config(['$interpolateProvider',
  function($interpolateProvider) {
        $interpolateProvider.startSymbol('{[{');
        $interpolateProvider.endSymbol('}]}');
  }
]);

app.controller('schedulerCtrl', function($scope, $http) {

    $(document).ready(function(){
      $(document).on('keyup', '#searchfield', function(event){
        if (event.which==13){
          $('#searchbtn').click();
          $('#searchfield').val('');
          $('.ui-autocomplete').hide();
        }
      });
	  $('#networkselect').on('change', function(event){
	  	$scope.getNetId($('#networkselect').val());
	  });
	  $('#termselect').on('change', function(event){
	  	$scope.getTermId($('#termselect').val() , $('#networkselect').val());
	  });
    });
    $scope.terms = [];
    $scope.klasses = [];
    $scope.getTerms = function(network_id){
	    $http.get('/scheduler/schedule/getTerms?id=' + network_id)
	    	.success(function(data, status, headers, config) {
	    		$scope.terms.splice(0);
	        	$scope.terms = data;
	    	});
    };
    $scope.getKlasses = function(term_id){
	    $http.get('/scheduler/schedule/getKlasses?id=' + term_id)
	    	.success(function(data, status, headers, config) {
	    		$scope.klasses.splice(0);
	        	$scope.klasses = data;
	        	console.log($scope.klasses);
			      $( "#searchbox" ).autocomplete({
			      	source: $scope.klasses
			      });
	    	});
    };
    $scope.getNetId = function(title){
	    $http.get('/scheduler/schedule/getNetId?str=' + title)
	    	.success(function(data, status, headers, config) {
	    		$scope.netId = data;
	    		$scope.getTerms($scope.netId);
	    	});
    };
    $scope.getTermId = function(term, network){
	    $http.get('/scheduler/schedule/getTermId?str=' + term +'&id=' + $scope.netId)
	    	.success(function(data, status, headers, config) {
	    		console.log(data);
	    		$scope.termId = data;
	    		$scope.getKlasses($scope.termId);
	    	});
    };
	$scope.events = [];
	$scope.eventSources = [
		$scope.events,
	];
	$scope.klasses = [];
	/* config object */
	$scope.uiConfig = {
	  calendar:{
		defaultView: 'agendaWeek',
	    minTime: '8:00 am',
	    maxTime: '8:00 pm',
	    header:{
	      left: '',
	      center: '',
	      right: '',
        },
        contentHeight: 1000,
	    editable: false,
	    allDaySlot: false,
		viewRender: function(view, element) {
			$http.get('getTimeslots')
				.success(function(data, status, headers, config) {
				  	view.calendar.removeEventSource($scope.events);
				  	$scope.events.splice(0);
				  	angular.forEach(data,function(evt){
				  		startOfWeek = moment().startOf('week');
				  		title = evt.title,
				  		day = startOfWeek.add(evt.meet_day, 'days');
				  		start = moment(day.format('YYYY-MM-DD:Z') + ' ' + evt.start_time, 'YYYY-MM-DD:Z H:mm:ss');
				  		end = moment(day.format('YYYY-MM-DD:Z') + ' ' + evt.end_time, 'YYYY-MM-DD:Z H:mm:ss');
				  		$scope.events.push({
				  			title: title,
				  			description: evt.teacher,
				  			start: start.format(),
				  			end: end.format(),
				  			allDay: false,
				  		});
				  	});
				  	view.calendar.addEventSource($scope.events);
				});  
	  	},
        eventRender: function(event, element) { 
            element.find('.fc-event-title').append('<div class="eventDescription">' + event.description + '</div>'); 
        },
	  }
	};
});