(function () {
    var app = angular.module('nasMan', [
        'ng.django.urls',
        'ui-notification',
        'emguo.poller'
    ]);
    app.config(
        function ($httpProvider) {
            $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
        }
    );
    app.controller('NotificationCtrl', [
        '$http',
        '$scope',
        'Notification',
        'poller',
        'djangoUrl',
        function ($http, $scope, Notification, poller, djangoUrl) {
            scope = $scope;
            scope.count = -1;
            scope.notifications = [];
            var messageFetchUrl = djangoUrl.reverse(
                'notifications:messages-list');
            var notificationPoller = poller.get(
                messageFetchUrl,
                {
                    argumentsArray: [
                        {
                            params: {
                                since: new Date(0)
                            }
                        }
                    ]
                }
            );
            notificationPoller.promise.then(
                null,
                null,
                function (response) {
                    var data = response.data;
                    scope.notifications.push.apply(
                        scope.notifications,
                        data.results);
                    notificationPoller.argumentsArray[0].params.since = data.latest;
                    if (scope.count > -1 && data.results.length > 0) {
                        $(data.results).each(function (i, val) {
                            Notification(
                                {
                                    message: val.message,
                                    title: 'Notification'
                                },
                                'info'
                            );
                        });
                    }
                    scope.count += data.count;
                }
            );
        }
    ]);
})();
