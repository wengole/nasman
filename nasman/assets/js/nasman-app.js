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
            scope.count = null;
            scope.notifications = [];
            var messageFetchUrl = djangoUrl.reverse(
                'api:notifications-list');
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
                    if (scope.count != null && data.results.length > 0) {
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
                    if (scope.count === null) {
                        scope.count = 0;
                    }
                    scope.count += data.count;
                }
            );
        }
    ]);
})();
