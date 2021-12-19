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
    $scope.getUsers = function () {
            $http({
                method: 'GET',
                url: '/accounts/get_users',
            }).then(function successCallback(response) {
                $scope.users = response.data.users
            }, function errorCallback(response) {
                $scope.error = response.data.message
            });
    }
    
    $scope.getReview = function () {
        $http({
            method: 'GET',
            url: '/get_reviews',
        }).then(function successCallback(response) {
            $scope.reviews = response.data.reviews
        }, function errorCallback(response) {
            $scope.error = response.data.message
        });
    }
    
    $scope.deleteUser = function (userId) {
        $http({
            method: 'DELETE',
            url: '/accounts/delete_user',
            params: {
                user_id: userId
            }
        }).then(function successCallback(response) {
            $scope.getUsers();
        }, function errorCallback(response) {
            $scope.error = response.data.message
        });
    }
    
        $scope.getStats = function () {
        $http({
            method: 'GET',
            url: '/get_stats',
        }).then(function successCallback(response) {
            $scope.amountUsers = response.data.amount_users;
            $scope.amountPosts = response.data.amount_posts;
            $scope.amountReviews = response.data.amount_reviews;
        }, function errorCallback(response) {
            $scope.error = response.data.message
        });
    }
        $scope.getUsers();
        $scope.getReview();
        $scope.getStats();
    });

app.controller("homeCtrl", function ($scope, $http) {
    $scope.isAuthenticated = global.isAuthenticated;
    $scope.username = global.username;
    $scope.categories = [];
    $scope.postData = {};
    $scope.reviewData = {};
    $scope.uploadedImage = undefined;
    $scope.error = '';
    $scope.posts = [];
    $scope.currentCategory = '';
    $scope.showMyPosts = false;
    $scope.showFavorites = false;
    $scope.postToEdit = {};
    $scope.profileData= {};
    $scope.profileToEdit = {};
    $scope.postToShowContacts = {};
    $scope.isSuperuser = global.isSuperuser;
    $scope.search = '';
