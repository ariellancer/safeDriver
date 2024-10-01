import React, {useState, useEffect} from 'react';
import {View, Text, TouchableOpacity, StyleSheet, Image} from 'react-native';
import {useNavigation, useRoute} from '@react-navigation/native';
import back from '../tools/back.png';
//import statisticsPic from '../tools/your_statistics.png';
import CameraBackgroundCapture from '../tools/CameraBackgroundCapture'

export default function StatisticsPage() {
    const navigation = useNavigation();
    const route = useRoute();
    var {finalSeconds, isDriving, toSend, prev, token, type} = route.params;
    const currentDate = new Date();
    const [statisticsPic, setStatisticsPic] = useState(null);
    prevTimer = currentDate.getTime();
    const navigateToMenu = () => {
        if (isDriving) {
            const currentDate = new Date();
            currentTimer = currentDate.getTime();
            newFinalSeconds = finalSeconds + Math.floor((currentTimer - prevTimer) / 1000);
        } else {
            newFinalSeconds = finalSeconds;
        }
        navigation.navigate('Menu', {finalSeconds: newFinalSeconds, isDriving, toSend, prev, token, type});
    };
    const fetchDataFromServer = async () => {
        try {
            const res = await fetch('https://3e10-2a05-bb80-3a-8cba-c86b-65f0-97e-2b19.ngrok-free.app/api/Statistics', {
                method: 'get',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': JSON.stringify(token),
                },
            });
            if (res.status === 200) {
                const data = await res.json();
                const base64Image = `data:image/png;base64,${data.img}`;
                setStatisticsPic(base64Image);
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
                    <Image source={back} style={styles.backImage}/>
                </TouchableOpacity>
                <Text style={styles.text}>Your Statistics</Text>
                {statisticsPic && (<Image source={{uri: statisticsPic}} style={styles.image}
                    />
                )}
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
        marginTop: 100,
        fontSize: 30,
        fontWeight: 'bold',
    },
});
