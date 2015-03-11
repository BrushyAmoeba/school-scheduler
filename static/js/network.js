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
	$scope.loadSection = function(section){
    	$scope.section = section;
    };
    $scope.checkSection = function(section){
    	return $scope.section==section;
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
    $scope.createNetwork = function(){
    	var input = $('#network').find('input');
		$http.post('/scheduler/manager/createNetwork', {title: input.val()})
  			.success(function(data, status, headers, config) {
    			$scope.networks.push(data);
          		input.val('');
  			});
    };
});