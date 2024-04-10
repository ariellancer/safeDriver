import { Camera, CameraType } from 'expo-camera';
import { useState } from 'react';
import { Pressable,Button, StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { useNavigation, useRoute } from '@react-navigation/native';
import CameraBackgroundCapture from '../tools/CameraBackgroundCapture'
var numOfUnfocused = 0;
newFinalSeconds=0
export default function App() {
  const navigation = useNavigation();
  const [type, setType] = useState(CameraType.back);
  const [permission, requestPermission] = Camera.useCameraPermissions();
  const route = useRoute();
  var {finalSeconds,isDriving,toSend,prev,token} = route.params;
  numOfUnfocused = prev;
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
    navigation.navigate('Menu',{finalSeconds: newFinalSeconds,isDriving,toSend,prev:numOfUnfocused,token});
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
  const addUnfocused = ()=>{
    numOfUnfocused+=1;
    
  }
  function toggleCameraType() {
    setType(current => (current === CameraType.back ? CameraType.front : CameraType.back));
  }
  return (
    <View style={styles.container}>
      {isDriving ? <CameraBackgroundCapture updateVal={addUnfocused} style={styles.camera} type={type} token={token}/>:<Camera style={styles.camera} type={type} />}
      <View style={styles.buttonContainer}>
        <Pressable style={styles.backButton} onPress={navigateToMenu}>
          <Text style={styles.text}>Back to Menu</Text>
        </Pressable>
        <TouchableOpacity style={styles.cameraButton} onPress={toggleCameraType}>
          <Text style={styles.text}>Flip Camera</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  camera: {
    flex: 1,
  },
  buttonContainer: {
    position: 'absolute',
    bottom: 16,
    left: 16,
    right: 16,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  backButton: {
    padding: 10,
    borderRadius: 8,
    backgroundColor: '#4CAF50',
  },
  cameraButton: {
    padding: 10,
    borderRadius: 8,
    backgroundColor: '#FF5733',
  },
  text: {
    fontSize: 18,
    fontWeight: 'bold',
    color: 'white',
  },
});
