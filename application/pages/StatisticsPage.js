import React, { useState, useEffect } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Image } from 'react-native';
import { useNavigation, useRoute } from '@react-navigation/native';
import back from '../tools/back.png';
import statisticsPic from '../tools/your_statistics.png';

export default function StatisticsPage() {
  const navigation = useNavigation();
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
  return (
    <>
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
