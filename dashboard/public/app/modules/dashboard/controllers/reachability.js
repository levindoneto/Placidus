dashboard.controller(
    'reachabilityController', [
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
            const verifications = firebase.database().ref(`/users/${$scope.userId}/verifications/reachability`);
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
                $scope.availableOptions = $scope.currentTopology.availableOptions;
                $scope.topologyLinks = $scope.currentTopology.links;
            });

            $scope.modal = function(id) {
                $scope.currentVerification = $scope.verificationsObj[id];
            };

            $scope.verifyReachability = function() {
                console.log('$scope.topologyLinks: ', $scope.topologyLinks);
                swal({
                    title: "Currently just via API, soon on the dashboard."
                });
                swal({
                    title: "Name the Verification",
                    text: "The name is used as a verification identifier",
                    input: 'text',
                    showCancelButton: true,
                    inputPlaceholder: 'Verification '.concat(verificationsList.length + 1)
                }).then(function(inputValue) {
                    inputValue = inputValue? inputValue: 'Verification '.concat(verificationsList.length + 1);
                    swal({
                        title: 'Origin Device',
                        input: 'select',
                        inputOptions: $scope.availableOptions,
                        inputPlaceholder: 'Select Origin',
                        showCancelButton: true
                      }).then(function (origin) {
                            if(0 === origin.length) $scope.verifyReachability();
                            swal({
                                title: 'Destination Device',
                                input: 'select',
                                inputOptions: $scope.availableOptions,
                                inputPlaceholder: 'Select Destination',
                                showCancelButton: true
                            }).then(function (destination) {
                                swal({
                                        title: 'Are you sure you want to verify reachability for [' + origin + ']->['+destination+
                                         '] in the topology '.concat($scope.currentTopology.fullName, '?'),
                                        showCancelButton: true,
                                        confirmButtonText: 'Yes',
                                        cancelButtonText: 'Cancel',
                                        showLoaderOnConfirm: true,
                                        preConfirm: function(result) {
                                            return new Promise(function(resolve, reject) {
                                                if (result) {
                                                    axios.post('http://dawntech.brazilsouth.cloudapp.azure.com:8060/reachability', {
                                                        data: {
                                                            'origin': origin,
                                                            'destination': destination,
                                                            'topologyLinks': $scope.topologyLinks
                                                        }
                                                    })
                                                    .then(function(response){
                                                        // save db
                                                        response.data.name = inputValue;
                                                        response.data.when = new Date().toString();
                                                        response.data.topologyId = $scope.currentTopologyId;
                                                        verificationsList.$add(response.data).then((verificationId) => {
                                                            auxVid = verificationId.toString().split('/');
                                                            verificationId = auxVid[auxVid[auxVid.length-1]];
                                                            swal({
                                                                title: 'The reachability from the topology '.concat($scope.currentTopology.fullName, ' has been successfully verified!'),
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
                                                            title: 'Error on verifying reachability of the topology '.concat($scope.currentTopology.fullName),
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
                            })
                      })
                });
            };

            $scope.redirectToFormalVerification = function() {
                $state.go('app.formalVerification');
            };

            $scope.redirectToFormalVerificationTopology = function() {
                $state.go('app.formalVerificationTopology');
            };
        }
    ]
);
