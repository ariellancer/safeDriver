import { Camera, CameraType } from 'expo-camera';
import { useState } from 'react';
import { Pressable,Button, StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { useNavigation, useRoute } from '@react-navigation/native';
export default function App() {
  const navigation = useNavigation();
  const [type, setType] = useState(CameraType.back);
  const [permission, requestPermission] = Camera.useCameraPermissions();
  const route = useRoute();
  var {finalSeconds,isDriving} = route.params;
  const currentDate = new Date();
  prevTimer = currentDate.getTime();
  const navigateToMenu = () => {
    if(isDriving){
      const currentDate = new Date();
      currentTimer = currentDate.getTime();
      newFinalSeconds = finalSeconds + Math.floor((currentTimer - prevTimer)/1000);
    }else{
      newFinalSeconds = finalSeconds;
    } 
    navigation.navigate('Menu',{finalSeconds: newFinalSeconds,isDriving});
  };
  if (!permission) {
    // Camera permissions are still loading
    return <View />;
  }

  if (!permission.granted) {
    // Camera permissions are not granted yet
    return (
      <View style={styles.container}>
        <Text style={{ textAlign: 'center' }}>We need your permission to show the camera</Text>
        <Button onPress={requestPermission} title="grant permission" />
      </View>
    );
  }

  function toggleCameraType() {
    setType(current => (current === CameraType.back ? CameraType.front : CameraType.back));
  }

  return (
    <View style={styles.container}>
      <Camera style={styles.camera} type={type}>
        <View style={styles.buttonContainer}>
          <TouchableOpacity style={styles.cameraButton} onPress={toggleCameraType}>
            <Text style={styles.text}>Flip Camera</Text>
          </TouchableOpacity>
          <Pressable style={styles.backButton} onPress={navigateToMenu} >
            <Text style={styles.text} > Back to Menu</Text>
          </Pressable>
        </View>
      </Camera>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
  },
  camera: {
    flex: 1,
  },
  backButton: {
  },
  buttonContainer: {
    flex: 1,
    flexDirection: 'row',
    backgroundColor: 'transparent',
    margin: 64,
  },
  cameraButton: {
    flex: 1,
    alignSelf: 'flex-end',
    alignItems: 'center',
    marginTop: '10',
  },
  text: {
    fontSize: 24,
    fontWeight: 'bold',
    color: 'white',
  },
});
