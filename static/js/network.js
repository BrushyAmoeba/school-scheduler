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
			title: input.val()
		}).success(function(data, status, headers, config) {
			$scope.networks.push(data);
      		input.val('');
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
});