(function () {
    var app = angular.module('nasMan', []);

    app.controller('NotificationCtrl', ['$http', '$scope', function ($http, $scope) {
        $scope.count = 0;
        $scope.notifications = [];
        $http.get('/notifications/messages/').success(
            function (data) {
                $scope.notifications = data.results;
                $scope.count = data.count;
            }
        )
    }]);
})();

