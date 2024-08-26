import React, { useEffect, useRef,useState } from 'react';
import { Platform,StyleSheet } from 'react-native';
import { Camera, CameraType } from 'expo-camera/legacy';
import { Audio } from 'expo-av';
const CameraBackgroundCapture = ({updateVal,style,token}) => {
const [type, setType] = useState(CameraType.front); // change to front
const cameraRef = useRef(null);
// Function to make the phone beep
const makeBeep = async () => {
  const soundObject = new Audio.Sound();
  try {
    await soundObject.loadAsync(require('../tools/beep-04.mp3'));
    await soundObject.setIsLoopingAsync(true); // Set looping to true
    await soundObject.playAsync();
    setTimeout(async () => {
      await soundObject.stopAsync();
      await soundObject.unloadAsync();
    }, 5000); // Stop the loop after 5 seconds
  } catch (error) {
    console.error('Failed to play chirp sound', error);
  }
};
  useEffect(() => {
    const takePicture = async () => {
      if (Platform.OS === 'android') {
        // Request permission for Android
        const { status } = await  Camera.requestMicrophonePermissionsAsync();;
        if (status !== 'granted') {
          return;
        }
      }
      try{
      if (cameraRef.current) {
        const options = { quality: 1, base64: true };
        var pictures =[]
        for (let i = 0; i < 3; i++) {
          const data = await cameraRef.current.takePictureAsync(options);
          const start = Date.now();
          pictures.push(data.base64);
          while (Date.now() - start < 750) {}//3/4 sec between each picture
        }
        try{
          const check = {
            pictures:pictures
          }
          const res = await fetch('https://7ca1-2a05-bb80-8-f754-8d10-216f-1333-8db7.ngrok-free.app/api/Model', {
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
            console.log(temp.result)
            if(temp.result === 0){
              updateVal();
              makeBeep();
            }
          }
      }catch(error){
        console.log(error);
      }
      }
    }catch(error){
      console.log("error back")
    }
    };

    const timer = setInterval(() => {
      takePicture();
    }, 10000); // Every 10 seconds

    return () => {
      clearInterval(timer);
    };
  }, []);
  return (
<Camera
  ref={cameraRef}
  style={style}
  type={type}
/>
  );
};
export default CameraBackgroundCapture;