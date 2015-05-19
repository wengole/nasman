/**
 * MainCtrl - controller
 */
function MainCtrl() {

    this.userName = 'Example user';
    this.helloText = 'Welcome in SeedProject';
    this.descriptionText = 'It is an application skeleton for a typical AngularJS web app. You can use it to quickly bootstrap your angular webapp projects and dev environment for these projects.';

}


function NotificationCtrl($scope, poller) {
    scope = $scope;
    scope.count = null;
    scope.messages = [];
    var notificationPoller = poller.get(
        '/api/notifications/');
    notificationPoller.promise.then(
        null,
        null,
        function (response) {
            var data = response.data;
            scope.messages = data.results;
            scope.latest = data.latest;
            scope.count = data.count;
        });
}

angular
    .module('inspinia')
    .controller('MainCtrl', MainCtrl)
    .controller('NotificationCtrl', NotificationCtrl);
