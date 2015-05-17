/**
 * INSPINIA - Responsive Admin Theme
 * Copyright 2015 Webapplayers.com
 *
 * Inspinia theme use AngularUI Router to manage routing and views
 * Each view are defined as state.
 * Initial there are written state for all view in theme.
 *
 */
function config($stateProvider, $urlRouterProvider, $ocLazyLoadProvider) {
    $urlRouterProvider.otherwise("/index/main");

    $ocLazyLoadProvider.config({
        // Set to true if you want to see what and when is dynamically loaded
        debug: false
    });

    $stateProvider

        .state('index', {
            abstract: true,
            url: "/index",
            templateUrl: "static/core/views/common/content.html",
        })
        .state('index.main', {
            url: "/main",
            templateUrl: "static/core/views/main.html",
            data: {pageTitle: 'Example view'}
        })
        .state('index.minor', {
            url: "/minor",
            templateUrl: "static/core/views/minor.html",
            data: {pageTitle: 'Example view'}
        })
}
angular
    .module('inspinia')
    .config(config)
    .run(function ($rootScope, $state) {
             $rootScope.$state = $state;
         });
