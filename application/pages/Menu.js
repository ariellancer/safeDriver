import React, { useEffect, useRef } from 'react';
import { View, Text, TouchableOpacity, StyleSheet} from 'react-native';
import { useNavigation ,useRoute} from '@react-navigation/native';
import CameraBackgroundCapture from '../tools/CameraBackgroundCapture'
export default function Menu() {
  const navigation = useNavigation();
  const route = useRoute();
  var {finalSeconds,isDriving} = route.params;
  const currentDate = new Date();
  prevTimer = currentDate.getTime();
  const navigateToDriving = () => {
    if(isDriving){
      const currentDate = new Date();
      currentTimer = currentDate.getTime();
      newFinalSeconds = finalSeconds + Math.floor((currentTimer - prevTimer)/1000);
    }else{
      newFinalSeconds = finalSeconds;
    } 
    navigation.navigate('StartDriving',{finalSeconds: newFinalSeconds,isDriving});
  };
  const navigateToCamera = () => {
    navigation.navigate('Camera',{finalSeconds: newFinalSeconds,isDriving});
  };
  const navigateToStatistics = () => {
    if(isDriving){
      const currentDate = new Date();
      currentTimer = currentDate.getTime();
      newFinalSeconds = finalSeconds + Math.floor((currentTimer - prevTimer)/1000);
    }else{
      newFinalSeconds = finalSeconds;
    } 
    navigation.navigate('StatisticsPage',{finalSeconds: newFinalSeconds,isDriving});
  };

  const handleLogout = () => {
    navigation.navigate('Login');
  };
  return (
    <>
    {isDrivingNew &&  <CameraBackgroundCapture/> }
    <View style={styles.container}>
      <TouchableOpacity style={styles.mainButton} onPress={navigateToDriving}>
         <Text style={styles.buttonText}>To start driving</Text>
      </TouchableOpacity>
      <TouchableOpacity style={styles.mainButton} onPress={navigateToStatistics}>
        <Text style={styles.buttonText}>To your statistics</Text>
      </TouchableOpacity>
      <TouchableOpacity style={styles.mainButton} onPress={navigateToCamera}>
        <Text style={styles.buttonText}>Camera direction</Text>
      </TouchableOpacity>
      <TouchableOpacity style={styles.logout} onPress={handleLogout}>
        <Text style={styles.buttonText}>Logout</Text>
      </TouchableOpacity>
    </View>
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
  
});
