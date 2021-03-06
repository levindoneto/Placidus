dashboard.controller(
    'redundanciesFirewallController', [
        '$scope',
        '$firebaseObject',
        '$firebaseArray',
        '$rootScope',
        '$state',
        function (
            $scope,
            $firebaseObject,
            $firebaseArray,
            $rootScope,
            $state
        ) {
            const vm = this;
            
            $scope.userId = $rootScope.userDB?$rootScope.userDB.uid: localStorage.loggedUser;
            const verifications = firebase.database().ref(`/users/${$scope.userId}/verifications/firewall/redundancies`);
            const verificationsList = $firebaseArray(verifications);
            const verificationsObj = $firebaseObject(verifications);
            verificationsList.$loaded().then(() => {
                $scope.verifications = verificationsList;
                $scope.verificationsObj = verificationsObj;
            });

            const topologies = firebase.database().ref(`/users/${$scope.userId}/topologies/`);
            const topologiesList = $firebaseArray(topologies);
            const topologiesObj = $firebaseObject(topologies);
            
            topologiesList.$loaded().then(() => {
                $scope.topologies = topologiesObj;
                $scope.currentTopologyId = topologiesObj.currentTopologyId;
                $scope.currentTopology = topologiesObj[$scope.currentTopologyId];
                console.log('$scope.currentTopology: ', $scope.currentTopology);
            });


            $scope.modal = function(id) {
                $scope.currentVerification = $scope.verificationsObj[id];
            };

            $scope.verifyRulesFirewall = function() {
                swal({
                    title: "Name the Verification",
                    text: "The name is used as a verification identifier",
                    input: 'text',
                    showCancelButton: true,
                    inputPlaceholder: 'Verification '.concat(verificationsList.length + 1)
                }).then(function(inputValue) {
                    inputValue = inputValue? inputValue: 'Verification '.concat(verificationsList.length + 1);
                    swal({
                        title: 'Are you sure you want to verify redundancies in the firewalls of the topology '.concat($scope.currentTopology.fullName, '?'),
                        showCancelButton: true,
                        confirmButtonText: 'Yes',
                        cancelButtonText: 'Cancel',
                        showLoaderOnConfirm: true,
                        preConfirm: function(result) {
                            return new Promise(function(resolve, reject) {
                                if (result) {
                                    axios.get('http://dawntech.brazilsouth.cloudapp.azure.com:8060/rules/firewall/redundancies')
                                    .then(function(response){
                                        // save db
                                        response.data.name = inputValue;
                                        response.data.when = new Date().toString();
                                        response.data.topologyId = $scope.currentTopologyId;
                                        verificationsList.$add(response.data).then((verificationId) => {
                                            auxVid = verificationId.toString().split('/');
                                            verificationId = auxVid[auxVid[auxVid.length-1]];
                                            swal({
                                                title: 'The firewalls from the topology '.concat($scope.currentTopology.fullName, ' have been successfully verified!'),
                                                text: (response.data.status).concat('\n', 'To check out the details, please check the verification history'),
                                                icon: 'success',
                                                showCancelButton: true,
                                                confirmButtonText: 'Ok',
                                                cancelButtonText: 'Cancel',
                                                timer: 10000
                                            }).then(function(ok) {
                                                $scope.modal(verificationId);
                                            });
                                        });
                                    })
                                    .catch(function(error){
                                        swal({
                                            title: 'Error on verifying redundancies in the firewalls of the topology '.concat($scope.currentTopology.fullName),
                                            text: 'Please check its details and try again.',
                                            icon: 'error',
                                            button: false,
                                            timer: 5000
                                        });
                                    })
                                }
                            });
                        },
                        allowOutsideClick: () => !swal.isLoading(),
                    });
                });
            };

            $scope.redirectToFormalVerification = function() {
                $state.go('app.formalVerification');
            };

            $scope.redirectToFormalVerificationFirewall = function() {
                $state.go('app.formalVerificationFirewall');
            };
        }
    ]
);
