import React, { useEffect, useRef,useState } from 'react';
import { Platform,StyleSheet } from 'react-native';
import { Camera, CameraType } from 'expo-camera/legacy';
import { Audio } from 'expo-av';
import {BASE_URL} from "../config";
UNFOCUSED = 0;
const CameraBackgroundCapture = ({updateVal,style,type,token}) => {

    const [currentType, setType] = useState(type); // Type camera (front or back)
    const cameraRef = useRef(null);

    // Function to make the phone beep
    const makeBeep = async () => {
        const soundObject = new Audio.Sound();
        try {
            await soundObject.loadAsync(require('../tools/beep-04.mp3')); // load the audio
            await soundObject.setIsLoopingAsync(true); // set to playing in loop
            await soundObject.playAsync(); // playing in async.
            setTimeout(async () => { // Stop the beep after 2.5 seconds
                await soundObject.stopAsync();
                await soundObject.unloadAsync();
            }, 2500);
        } catch (error) {
            console.error('Failed to play chirp sound', error);
        }
    };
    useEffect(() => {
        // take a picture and send to server to analyze.
        const takePicture = async () => {
            // Request permission for Android
            if (Platform.OS === 'android') {
                const { status } = await  Camera.requestMicrophonePermissionsAsync();;
                if (status !== 'granted') {
                    return;
                }
            }
            try{
                if (cameraRef.current) { // make sure the have a reference to camera
                    const options = { quality: 0.75, base64: true };
                    var pictures =[]
                    // for (let i = 0; i < 2; i++) {
                    //   const data = await cameraRef.current.takePictureAsync(options);
                    //   const start = Date.now();
                    //   pictures.push(data.base64);
                    //   while (Date.now() - start < 750) {}//3/4 sec between each picture
                    // }
                    const data = await cameraRef.current.takePictureAsync(options);
                    pictures.push(data.base64);
                    try{
                        const check = {
                        pictures:pictures
                        }
                        const res = await fetch(`${BASE_URL}/api/Model`, {
                            'method': 'POST',
                            'headers':{
                            'Content-Type': 'application/json',
                            'authorization': JSON.stringify(token),
                            },
                            'body': JSON.stringify(check)
                        })
                        if(res.status === 200){
                            var temp = await res.text();
                            temp = JSON.parse(temp);
                            if(temp.result === UNFOCUSED){
                                updateVal(); // add 1 to unfocused times.
                                makeBeep();
                            }
                        }
                    }catch(error){
                        console.log("error in sending to server ");
                    }
                }
            }catch(error){
                console.log("error in taking a pictures")
            }
        };
        const timer = setInterval(() => {
            takePicture();
        }, 5000); // play take picture function every 5 seconds.
        return () => { // stop taking pictures when the component is unmounted.
            clearInterval(timer);
        };
    }, []); // play once when the component mounts
    return (
             <Camera
                ref={cameraRef}
                style={style}
                type={currentType}
             />
    );
};
export default CameraBackgroundCapture;