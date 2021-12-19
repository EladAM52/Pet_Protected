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

app.controller("loginCtrl", function ($scope, $http, $window) {
    $scope.data = {};
    $scope.error = '';

    $scope.submit = function () {
        $scope.error = '';
        $http({
            method: 'POST',
            url: '/accounts/login',
            data: $scope.data
        }).then(function successCallback(response) {
            $window.location.href = '/'; // redirect to home page
        }, function errorCallback(response) {
            $scope.error = response.data.message
        });
    }
});

app.controller("registerCtrl", function ($scope, $http, $window) {
    $scope.data = {};
    $scope.error = '';

    $scope.submit = function () {
        $scope.error = '';
        $http({
            method: 'POST',
            url: '/accounts/register',
            data: $scope.data
        }).then(function successCallback(response) {
            $window.location.href = '/'; // redirect to home page
        }, function errorCallback(response) {
            $scope.error = response.data.message
        });
    }
});
app.controller("managementCtrl", function ($scope, $http, $window) {
    $scope.users = [];
    $scope.error = "";
    $scope.amountUsers = 0;
    $scope.amountPosts = 0;
    $scope.amountReviews = 0;
}
