var app = angular.module('scheduler', ['ui.calendar']);

app.config(['$interpolateProvider',
  function($interpolateProvider) {
        $interpolateProvider.startSymbol('{[{');
        $interpolateProvider.endSymbol('}]}');
  }
]);


app.controller('schedulerCtrl', function($scope, $http) {
	/* config object */
	$scope.events = [
			{
				title: 'Test',
				start: new Date(2015,2,1),
			},
			{
				title: 'Test2',
				start: new Date(2015,3,1),
			}
		];
	$scope.eventSources = [
		$scope.events,
	];

	$http.get('getTimeslots')
		.success(function(data, status, headers, config) {
		  	$scope.eventSources = [];
		  	events = [];
		  	startOfWeek = moment().startOf('week');
		  	angular.forEach(data,function(evt){
		  		day = startOfWeek.add(evt.meet_day, 'days');
		  		console.log(evt);
		  		start = moment(day.format('YYYY-MM-DD:Z') + ' ' + evt.start_time, 'YYYY-MM-DD:Z H:mm:ss');
		  		console.log(start.format());
		  		events.push({
		  			title: 'hello',
		  			start: "2015-03-02T14:00:00-08:00",
		  			end: "2015-03-02T14:20:00-08:00",
		  			
		  			allDay: false,
		  		});
		  	});
		  	$scope.eventSources.push(events);
		});

	$scope.uiConfig = {
	  calendar:{
	    height: 500,
	    defaultView: 'agendaWeek',
	  }
	};
});