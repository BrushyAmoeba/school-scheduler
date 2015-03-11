var app = angular.module('scheduler', ['ui.directives']);

app.config(['$interpolateProvider',
  function($interpolateProvider) {
        $interpolateProvider.startSymbol('{[{');
        $interpolateProvider.endSymbol('}]}');
  }
]);

app.controller('schedulerCtrl', function($scope, $http) {
    $( "#search input" ).autocomplete({
      source: classes
    });
    $(document).ready(function(){
      $(document).on('keyup', '#searchfield', function(event){
        if (event.which==13){
          $('#searchbtn').click();
          $('#searchfield').val('');
          $('.ui-autocomplete').hide();
        }
      });
    });
    $scope.loadSection = function(section){
      $scope.section = section;
    }
    $scope.checkSection = function(section){
      return $scope.section==section;
    }
	/* config object */
	$scope.events = [];
	$scope.eventSources = [
		$scope.events,
	];
	$scope.klasses = [];

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