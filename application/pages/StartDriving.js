import React, { useState, useEffect, useRef } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Image } from 'react-native';
import { useNavigation ,useRoute} from '@react-navigation/native';
import back from '../tools/back.png';
isDrivingNew = false;
toAdd = true
number = 0;
nhour =0
export default function StartDriving() {
  const navigation = useNavigation();
  const route = useRoute();
  const {finalSeconds,isDriving,prev,token} = route.params;

  if(toAdd){
    toAdd = false;
    newFinalSeconds = finalSeconds;
}
  const [timeNew, setTime] = useState({seconds:newFinalSeconds,minutes: Math.floor(newFinalSeconds / 60),hours:Math.floor(newFinalSeconds / 3600)});
  const currentDate = new Date();
  prevTimer = currentDate.getTime();
  useEffect(() => {
    let timeoutId;
    const updateTimer = () => {
      setTime((prevTime) => {
        const currentDate = new Date();
        currentTimer = currentDate.getTime();
        newFinalSeconds += Math.floor((currentTimer - prevTimer)/1000);
        prevTimer = currentTimer;
        return {
          seconds: newFinalSeconds,
          minutes: Math.floor(newFinalSeconds / 60),
          hours: Math.floor(newFinalSeconds / 3600),
        };
      });
      timeoutId = setTimeout(updateTimer, 1000);
    };
    if (isDrivingNew) {
      updateTimer();
    }
    return () => clearTimeout(timeoutId);
  }, [isDrivingNew]);
  const handleStartDriving = () => {
    const currentDate = new Date();
    nhour = currentDate.getHours();
    nminute= currentDate.getMinutes();
    nsecond = currentDate.getSeconds();
    isDrivingNew = true;
    setTime(({ hours: 0, minutes: 0, seconds: 0 }));
    newFinalSeconds = 0;
    prevTime = currentDate.getTime();
    toAdd = true;
    navigation.navigate('Menu',{finalSeconds:newFinalSeconds,isDriving:isDrivingNew,toSend:false,prev:0,token:token,hour:nhour})
  };
  const handleEndDriving = () => {
    isDrivingNew = false;
    toAdd = true;
    navigation.navigate('Menu',{finalSeconds:newFinalSeconds,isDriving:isDrivingNew,toSend:true,prev:prev,token,hour:nhour})
    //send to server the time and num of unfocused
  };
  const navigateToMenu = () => {
    toAdd = true;
    navigation.navigate('Menu',{finalSeconds:newFinalSeconds,isDriving:isDrivingNew,toSend:false,prev :prev,token,hour:nhour})
  };
  return (
    <>
      <View style={styles.container}>
        <View style={styles.timerContainer}>
          <Text style={styles.timerText}>{`${timeNew.hours < 10 ? '0' : ''}${timeNew.hours}:${(timeNew.minutes%60) < 10 ? '0' : ''}${timeNew.minutes%60}:${(timeNew.seconds%60) < 10 ? '0' : ''}${timeNew.seconds%60}`}</Text>
        </View>
        <View style={styles.numberOfNotFocus}>
          <Text style={styles.unFocusedText}>Unfocused: {prev}</Text>
        </View>
        <TouchableOpacity style={isDrivingNew? styles.endDrivingButton : styles.startDrivingButton} onPress={isDrivingNew ? handleEndDriving : handleStartDriving}>
          <Text style={styles.buttonText}>{isDrivingNew ? 'End Driving' : 'Start Driving'}</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.backButton} onPress={navigateToMenu}>
          <Image source={back} style={styles.backImage} />
        </TouchableOpacity>
      </View>
    </>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'flex-start',
    alignItems: 'center',
    backgroundColor: '#fff',
    paddingTop: 50,
  },
  numberOfNotFocus:{
    marginTop: 20,
    transform: [{ translateX: 0 }, { translateY: -10 }],
  },
  backButton: {
    position: 'absolute',
    top: 80,
    left: 10,
  },
  backImage: {
    width: 50,
    height: 50,
  },
  startDrivingButton: {
    backgroundColor: '#4CAF50',
    padding: 20,
    borderRadius: 50,
    justifyContent: 'center',
    alignItems: 'center',
    position: 'absolute',
    bottom: '50%', 
    left: '50%',    
    transform: [{ translateX: -125 }, { translateY: 220 }],  
    width: 250,
    height: 250,
  },
  endDrivingButton: {
    backgroundColor: 'red',
    padding: 20,
    borderRadius: 50,
    justifyContent: 'center',
    alignItems: 'center',
    position: 'absolute',
    bottom: '50%', 
    left: '50%',    
    transform: [{ translateX: -125 }, { translateY: 220 }],  
    width: 250,
    height: 250,
  },
  timerContainer: {
    marginTop: 20,
    transform: [{ translateX: 0 }, { translateY: 170 }],
  },
  timerText: {
    fontSize: 60,
    fontWeight: 'bold',
  },
  unFocusedText: {
    fontSize: 40,
    fontWeight: 'bold',
  },
  buttonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
});
