app.controller('appCtrl', ['$rootScope', '$scope', '$state', '$location', 'Flash', 'appSettings', '$firebaseAuth', '$firebaseObject',
function ($rootScope, $scope, $state, $location, Flash, appSettings, $firebaseAuth, $firebaseObject) {
    const vm = this;
    $rootScope.layout = appSettings.layout;
    vm.auth = $firebaseAuth();

    vm.auth.$onAuthStateChanged((firebaseUser) => {
        if (firebaseUser) {
            vm.currentUser = vm.auth.$getAuth();
            $rootScope.userDB = vm.currentUser;
            const refUser = firebase.database().ref(`users/${vm.currentUser.uid}`);
            const user = $firebaseObject(refUser);
            localStorage.setItem('loggedUser', vm.currentUser.uid);
            user.$loaded().then(() => {
                $rootScope.user = user;
                var alreadyExist = false;
            });
        } else {
            $state.go('login');
        }
    });

    //avalilable themes
    vm.themes = [
        {
            theme: 'blue',
            color: 'skin-blue-light',
            title: 'White and Blue',
            icon:'-o'
        }
    ];

    // Available layouts
    vm.layouts = [
        {
            name: 'Boxed',
            layout: 'layout-boxed'
        },
        {
            name: 'Fixed',
            layout: 'fixed'
        },
        {
            name: 'Sidebar Collapse',
            layout: 'sidebar-collapse'
        },
    ];

    vm.menuItems = [
        {
            title: 'Topologies',
            icon: 'table',
            state: 'topologies'
        },
        {
            title: 'Controller',
            icon: 'tablet',
            state: 'controller'
        },
        {
            title: 'Firewall',
            icon: 'shield',
            state: 'firewall'
        },
        {
            title: 'Formal Verification',
            icon: 'check-circle-o',
            state: 'formalVerification'
        },
    ];

    // Set the theme selected
    vm.setTheme = function (value) {
        $rootScope.theme = vm.themes[0];
    };


    // Set the Layout in normal view
    vm.setLayout = function (value) {
        $rootScope.layout = value;
    };


    // Controll sidebar open & close in mobile and normal view
    vm.sideBar = function (value) {
        if($(window).width()<=767){
            if ($('body').hasClass('sidebar-open'))
                $('body').removeClass('sidebar-open');
            else
                $('body').addClass('sidebar-open');
        } else {
            if(value==1){
                if ($('body').hasClass('sidebar-collapse'))
                    $('body').removeClass('sidebar-collapse');
                else
                    $('body').addClass('sidebar-collapse');
            }
        }
    };
}]);