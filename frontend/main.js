var app = angular.module('MovieRama', []);
app.controller('mainController',
	function($scope, $http) {
		$scope.loading = false;
		$scope.query;
		$scope.search = function(){
			$scope.loading = true;
			url = "http://localhost:8000/search/"+ $scope.query+"/?format=json" ;
			$http({
				method: 'GET',
				url: url
			}).success(function(data){
				$scope.loading = false;
				$scope.json = data;
			}).error(function(data){
				$scope.loading = false;
			})
		}
		$scope.now_playing = function(){

			$scope.loading = true;
			url = "http://localhost:8000/search/now_playing?format=json" ;
			$http({
				method: 'GET',
				url: url
			}).success(function(data){
				$scope.json = data;
				$scope.loading = false;
			}).error(function(data){
				$scope.loading = false;
			})
		}
	}
	);
