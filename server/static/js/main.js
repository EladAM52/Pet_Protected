const app = angular.module("myApp", []);

app.config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
});

app.config(['$httpProvider', function ($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

app.controller("navbarCtrl", function ($scope, $http, $window) {
    $scope.username = global.username;
    $scope.isAuthenticated = global.isAuthenticated;
    $scope.isSuperuser = global.isSuperuser;
});

