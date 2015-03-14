var app = angular.module('network', []);

app.config(['$interpolateProvider',
  function($interpolateProvider) {
        $interpolateProvider.startSymbol('{[{');
        $interpolateProvider.endSymbol('}]}');
  }
]);

app.controller('networkCtrl', function($scope, $http) {
	$scope.networks = networks;
	$scope.terms = [];
	$scope.klasses = [];
	$scope.timeslots = [];
	$scope.loadSection = function(section){
    	$scope.section = section;
    };
  $scope.checkSection = function(section){
  	return $scope.section==section;
  };
  $scope.createNetwork = function(){
  	var input = $('#network').find('input');
		$http.post('/scheduler/manager/createNetwork', {
			title: input.val(),
      user_id: user_id,
		}).success(function(data, status, headers, config) {
		  if (data != 'error'){
        $scope.networks.push(data);
        input.val('');          
      }
      else{
        alert('Network title already in use.');
      }
		});
  };
  $scope.viewNetwork = function(network_id){
    $http.get('/scheduler/manager/viewNetwork?id=' + network_id)
    	.success(function(data, status, headers, config) {
    		$scope.terms.splice(0);
        $scope.terms = data;
  			$scope.loadSection('term');
  			$scope.network_id = network_id;
    	});
  };
  $scope.removeNetwork = function(event, network_id){
    event.stopPropagation();
    $http.delete('/scheduler/manager/removeNetwork?id=' + network_id)
      .success(function(data, status, headers, config) {
        console.log('great success');
        network = _.findWhere($scope.networks, {network_id: network_id});
        $scope.networks.splice($scope.networks.indexOf(network),1);
      });
  }
	$scope.createTerm = function(){
    var input = $('#term').find('input');
		$http.post('/scheduler/manager/createTerm', {
			title: input.val(),
			network_id: $scope.network_id,
		}).success(function(data, status, headers, config) {
    		$scope.terms.push(data);
        input.val('');
  		});
    };
  $scope.viewTerm = function(term_id){
    $http.get('/scheduler/manager/viewTerm?id=' + term_id)
    	.success(function(data, status, headers, config) {
    		$scope.klasses.splice(0);
        $scope.klasses = data;
  			$scope.loadSection('class');
  			$scope.term_id = term_id;
    	});
  };
  $scope.removeTerm = function(event, term_id){
    event.stopPropagation();
    $http.delete('/scheduler/manager/removeTerm?id=' + term_id)
      .success(function(data, status, headers, config) {
        term = _.findWhere($scope.terms, {term_id: term_id});
        $scope.terms.splice($scope.terms.indexOf(term),1);
      });
  }
  $scope.createKlass = function(){
  	var title = $('#klasstitle');
  	var teacher = $('#teachername');
	$http.post('/scheduler/manager/createKlass', {
		title: title.val(),
		teacher: teacher.val(),
		term_id: $scope.term_id,
	}).success(function(data, status, headers, config) {
  		$scope.klasses.push(data);
        	title.val('');
        	teacher.val('');
		});
  };
  $scope.viewKlass = function(klass_id){
    $http.get('/scheduler/manager/viewKlass?id=' + klass_id)
    	.success(function(data, status, headers, config) {
    		$scope.timeslots.splice(0);
        	$scope.timeslots = data;
  			$scope.loadSection('timeslot');
  			$scope.klass_id = klass_id;
    	});
  };
  $scope.removeKlass = function(event, klass_id){
    event.stopPropagation();
    $http.delete('/scheduler/manager/removeKlass?id=' + klass_id)
      .success(function(data, status, headers, config) {
        klass = _.findWhere($scope.klasses, {klass_id: klass_id});
        $scope.klasses.splice($scope.klasses.indexOf(klass),1);
      });
  }
  $scope.createTimeslot = function(){
  	var meet_day = $('#meet_day');
  	var start = $('#start');
  	var end = $('#end');
	$http.post('/scheduler/manager/createTimeslot', {
		meet_day: meet_day.val(),
		start: start.val(),
		end: end.val(),
		klass_id: $scope.klass_id,
	}).success(function(data, status, headers, config) {
  		$scope.timeslots.push(data);
    	meet_day.val(1);
    	start.val('');
    	end.val('');
	  });
  };
  $scope.removeTimeslot = function(event, timeslot_id){
    event.stopPropagation();
    $http.delete('/scheduler/manager/removeTimeslot?id=' + timeslot_id)
      .success(function(data, status, headers, config) {
        timeslot = _.findWhere($scope.timeslots, {timeslot_id: timeslot_id});
        $scope.timeslots.splice($scope.timeslots.indexOf(timeslot),1);
      });
  }   
  $scope.numToDay = function(num){
  	if(num==1){return 'Monday'}
  	else if(num==2){return 'Tuesday'}
  	else if(num==3){return 'Wednesday'}
  	else if(num==4){return 'Thursday'}
  	else if(num==5){return 'Friday'}
  };
});


