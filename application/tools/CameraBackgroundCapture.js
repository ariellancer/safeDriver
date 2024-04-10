import React, { useEffect, useRef } from 'react';
import { Platform } from 'react-native';
import { Camera } from 'expo-camera';
import { Vibration } from 'react-native';
const CameraBackgroundCapture = ({updateVal,style,t,token}) => {
  const cameraRef = useRef(null);

// Function to make the phone beep
const makeBeep = () => {
  // Vibrate for 500 milliseconds
  Vibration.vibrate(1000);
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

      // Take picture using expo-camera
      if (cameraRef.current) {
        const options = { quality: 0.5, base64: true };
        var pictures =[]
        for (let i = 0; i < 3; i++) {
          // Take picture
          const data = await cameraRef.current.takePictureAsync(options);
          console.log(`Picture ${i + 1}: ${data.uri}`);
          const start = Date.now();
          pictures.push(data.base64);
          while (Date.now() - start < 750) {}
          //await new Promise(resolve => setTimeout(resolve, 750)); 
        }
        // send to server 3 pictures
        try{
          const check = {
            pictures:pictures
          }
          const res = await fetch('http://localhost:5000/api/Model/', {
            'method': 'get',
            'headers':{
                'Content-Type': 'application/json',
                'authorization': 'bearer ' + token,
              },
            'body': JSON.stringify(check)
          })
          if(res.status === 200){
            var temp = await res.text();
            temp = JSON.parse(temp);
            if(temp.result === 1){
              updateVal();
              makeBeep();
              //beep
            }
          }
      }catch(error){
        console.log(error);
      }
      updateVal(); //delete
      makeBeep();
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
  type={t}
/>

  );
};

export default CameraBackgroundCapture;
