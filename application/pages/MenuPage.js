import React from 'react';
import {useEffect, useRef, useState} from 'react'
import {View, Text, TouchableOpacity, StyleSheet} from 'react-native';
import {useNavigation, useRoute} from '@react-navigation/native';
import CameraBackgroundCapture from '../tools/CameraBackgroundCapture'

var numOfUnfocused = 0;
var toSendNew = true
send = false;
export default function MenuPage() {
    const navigation = useNavigation();
    const route = useRoute();
    const {finalSeconds, isDriving, toSend, prev, token, hour,type} = route.params;
    var Driving = isDriving;
    numOfUnfocused = prev == 0 ? 0 : numOfUnfocused < prev ? prev : numOfUnfocused;
    const [showModal, setShowModal] = useState(false);
    const [update, setUpdate] = useState(false);
    const [updateCounter, setUpdateCounter] = useState(0);
    const currentDate = new Date();
    prevTimer = currentDate.getTime();
    const navigateToDriving = () => {
        if (toSend && toSendNew) {
            setShowModal(true);
            return
        }
        if (isDriving) {
            const currentDate = new Date();
            currentTimer = currentDate.getTime();
            newFinalSeconds = finalSeconds + Math.floor((currentTimer - prevTimer) / 1000);
        } else {
            newFinalSeconds = finalSeconds;
        }
        toSendNew = true;
        send = false;
        navigation.navigate('StartDriving', {finalSeconds: newFinalSeconds, isDriving, prev: numOfUnfocused, token,type});
    };
    const navigateToCamera = () => {
        if (toSend && toSendNew) {
            setShowModal(true);
            return
        }
        toSendNew = true;
        const currentDate = new Date();
        prevTimer = currentDate.getTime();
        navigation.navigate('Camera', {
            finalSeconds: newFinalSeconds,
            isDriving,
            toSend: false,
            prev: numOfUnfocused,
            token,
            prevTimer,
            prevType: type
        });
    };
    const navigateToStatistics = () => {
        if (toSend && toSendNew) {
            setShowModal(true);
            return
        }
        if (isDriving) {
            const currentDate = new Date();
            currentTimer = currentDate.getTime();
            newFinalSeconds = finalSeconds + Math.floor((currentTimer - prevTimer) / 1000);
        } else {
            newFinalSeconds = finalSeconds;
        }
        toSendNew = true;
        navigation.navigate('StatisticsPage', {
            finalSeconds: newFinalSeconds,
            isDriving,
            toSend: false,
            prev: numOfUnfocused,
            token,
            type
        });
    };
    const addUnfocused = () => {
        numOfUnfocused += 1;

    }
    const handleLogout = () => {
        if ((toSend && toSendNew) || Driving) {
            setShowModal(true);
            return
        }
        toSendNew = true;
        navigation.navigate('Login');
    };
    const sendToServer = async () => {
        setUpdateCounter(updateCounter + 1);
        const currentDate = new Date();
        var nhour = currentDate.getHours();
        newDrive = {
            start: hour,
            end: nhour,
            unfocused: numOfUnfocused
        }
        try {
            const res = await fetch('https://3e10-2a05-bb80-3a-8cba-c86b-65f0-97e-2b19.ngrok-free.app/api/Statistics', {
                'method': 'PUT',
                'headers': {
                    'Content-Type': 'application/json',
                    'authorization': JSON.stringify(token),
                },
                'body': JSON.stringify(newDrive)
            })
            if (res.status === 200) {
                toSendNew = false;
                send = true;
                setUpdate(!update);
                setShowModal(false);
                numOfUnfocused = 0;
            } else {
                console.error("Error in sending to server")
            }
        } catch (error) {
            console.error(error);
        }
    };
    const ConfirmationModal = ({message, onConfirm, onCancel}) => {
        return (
            <View style={styles.modalContainer}>
                <View style={styles.modal}>
                    <View style={styles.modalContent}>
                        <Text>{message}</Text>
                        <View style={styles.buttonsContainer}>
                            <TouchableOpacity style={styles.button} onPress={onConfirm}>
                                <Text>Yes</Text>
                            </TouchableOpacity>
                            <TouchableOpacity style={styles.button} onPress={onCancel}>
                                <Text>No</Text>
                            </TouchableOpacity>
                        </View>
                    </View>
                </View>
            </View>
        );
    };
    const onConfirm = () => {
        toSendNew = false;
        setShowModal(false);
        if (Driving) {
            Driving = false
            handleLogout();
        }
    }
    const onCancel = () => {
        setShowModal(false);
    }
    return (
        <>
            {isDriving && (
                <CameraBackgroundCapture
                    updateVal={addUnfocused}
                    style={{position: 'absolute', bottom: 0, left: 0, width: 150, height: 200}}
                    type={type}
                    token={token}
                />
            )}
            <View style={styles.container}>
                <TouchableOpacity style={styles.mainButton} onPress={navigateToDriving}>
                    {isDriving ? <Text style={styles.buttonText}>Stop driving</Text> :
                        <Text style={styles.buttonText}>Start driving</Text>}
                </TouchableOpacity>
                <TouchableOpacity style={styles.mainButton} onPress={navigateToStatistics}>
                    <Text style={styles.buttonText}>To your statistics</Text>
                </TouchableOpacity>
                <TouchableOpacity style={styles.mainButton} onPress={navigateToCamera}>
                    <Text style={styles.buttonText}>Camera direction</Text>
                </TouchableOpacity>
                {toSend && (
                    <TouchableOpacity style={styles.mainButton} onPress={!send ? sendToServer : () => {
                    }}>
                        <Text style={styles.buttonText}>{!send ? "Send the result to server" : "sent"}</Text>
                    </TouchableOpacity>
                )}
                <TouchableOpacity style={styles.logout} onPress={handleLogout}>
                    <Text style={styles.buttonText}>Logout</Text>
                </TouchableOpacity>
            </View>
            {showModal && (
                <ConfirmationModal
                    message="You sure don't want to send??"
                    onConfirm={onConfirm}
                    onCancel={onCancel}
                />
            )}
        </>
    );

}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: '#fff',
    },
    mainButton: {
        backgroundColor: '#4CAF50',
        padding: 30,
        margin: 10,
        borderRadius: 12,
        width: '80%',
        alignItems: 'center',
    },
    logout: {
        backgroundColor: 'red',
        padding: 10,
        margin: 10,
        borderRadius: 12,
        position: 'absolute',
        top: 40,
        right: 7,
    },
    buttonText: {
        color: '#fff',
        fontSize: 18,
        fontWeight: 'bold',
    },
    modalContainer: {
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.5)',
        justifyContent: 'center',
        alignItems: 'center',
    },
    modal: {
        backgroundColor: '#fff',
        borderRadius: 8,
        padding: 20,
    },
    modalContent: {
        alignItems: 'center',
    },
    buttonsContainer: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        marginTop: 20,
    },
    button: {
        paddingVertical: 10, // Adjust as needed
        paddingHorizontal: 20, // Adjust as needed
    },

});
