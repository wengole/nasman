var NasManControllers = angular.module('NasManControllers', []);

NasManControllers.controller(
    'NotificationListCtrl',
    ['$scope', '$dragon',
        function ($scope, $dragon) {
            $scope.notifications = [];
            $scope.channel = 'notifications';

            $dragon.onReady(function () {
                $dragon.subscribe(
                    'notifications',
                    $scope.channel).then(
                    function (response) {
                        $scope.dataMapper = new DataMapper(response.data);
                    });

                $dragon.getList(
                    'notifications').then(
                    function (response) {
                        $scope.notifications = response.data;
                        $scope.notification_count = response.data.length;
                        $scope.plural = Boolean(response.data.length != 1);
                    });

                $dragon.callRouter('get_count', 'notifications').then(
                    function () {
                        $scope.notification_count = response.data.length;
                        $scope.plural = Boolean(response.data.length != 1);
                    }
                );
            });

            $dragon.onChannelMessage(
                function (channels, message) {
                    if (indexOf.call(channels, $scope.channel) > -1) {
                        $scope.$apply(function () {
                            $scope.dataMapper.mapData(
                                $scope.notifications,
                                message
                            );
                        });
                    }
                });

            $scope.itemDone = function (item) {
                item.done = true != item.done;
                $dragon.update(
                    'notifications',
                    item
                );
            }
        }]);
