var app = angular.module('network', []);

app.config(['$interpolateProvider',
  function($interpolateProvider) {
        $interpolateProvider.startSymbol('{[{');
        $interpolateProvider.endSymbol('}]}');
  }
]);

app.controller('networkCtrl', function($scope, $http) {
	$scope.loadSection = function(section){
      $scope.section = section;
    };
    $scope.checkSection = function(section){
      return $scope.section==section;
    };
});