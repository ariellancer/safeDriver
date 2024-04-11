import React, { useState, useEffect } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Image } from 'react-native';
import { useNavigation, useRoute } from '@react-navigation/native';
import back from '../tools/back.png';
import statisticsPic from '../tools/your_statistics.png';
import CameraBackgroundCapture from '../tools/CameraBackgroundCapture'
export default function StatisticsPage () {
  const navigation = useNavigation();
  const route = useRoute();
  var {finalSeconds,isDriving,toSend,prev,token} = route.params;
  const currentDate = new Date();
  prevTimer = currentDate.getTime();
  const navigateToMenu =  () => {
    if(isDriving){
      const currentDate = new Date();
      currentTimer = currentDate.getTime();
      newFinalSeconds = finalSeconds + Math.floor((currentTimer - prevTimer)/1000);
    }else{
      newFinalSeconds = finalSeconds;
    } 
    navigation.navigate('Menu',{finalSeconds: newFinalSeconds,isDriving,toSend,prev,token});
  };
  const fetchDataFromServer = async () => {
    try {
      const res = await fetch('http://localhost:5000/api/Statistics/' , {
        method: 'get',
        headers: {
          'Content-Type': 'application/json',
          'authorization': 'bearer ' + token,
        },
      });
      if (res.ok) {
        var data = await res.text();
        data = JSON.parse(date);
        statisticsPic=data.img
      } else {
        console.error('Failed to fetch data from the server');
      }
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  useEffect(() => {
    fetchDataFromServer(); // Fetch data when the component mounts
  }, []);
  return (
    <>
      {/* {isDriving &&  <CameraBackgroundCapture updateVal= {addUnfocused}/> } */}
      <View style={styles.container}>
        <TouchableOpacity style={styles.backButton} onPress={navigateToMenu}>
          <Image source={back} style={styles.backImage} />
        </TouchableOpacity>
        <Text  style={styles.text} >Your Statistics</Text>
        <Image source={statisticsPic} style={styles.image} />
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
  backButton: {
    position: 'absolute',
    top: 80,
    left: 10,
  },
  backImage: {
    width: 50,
    height: 50,
  },
  chart: {
    flex: 1,

  },
  image: {
    width: 380,
    height: 400,
    top: 100,
  },
  text: {
    marginTop:100,
    fontSize: 30,
    fontWeight: 'bold',
  },
});
