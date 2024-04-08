import React, { useEffect, useRef } from 'react';
import { Platform } from 'react-native';
import { Camera } from 'expo-camera';

const CameraBackgroundCapture = ({updateVal}) => {
  const cameraRef = useRef(null);
  useEffect(() => {
    const takePicture = async () => {
      if (Platform.OS === 'android') {
        // Request permission for Android
        const { status } = await Camera.requestMicrophonePermissionsAsync();
        if (status !== 'granted') {
          console.log('Camera permission denied');
          return;
        }
      }

      // Take picture using expo-camera
      if (cameraRef.current) {
        const options = { quality: 0.5, base64: true };
        for (let i = 0; i < 3; i++) {
          // Take picture
          const data = await cameraRef.current.takePictureAsync(options);
          console.log(`Picture ${i + 1}: ${data.uri}`);
          await new Promise(resolve => setTimeout(resolve, 750)); 
        }
        // send to server 3 pictures
        updateVal(prevValue => prevValue + 1); //if the server send not focus
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
  style={{ position: 'absolute', bottom: 0, left: 0, width: 150, height: 200 }}
  type={Camera.Constants.Type.back}
/>

  );
};

export default CameraBackgroundCapture;
