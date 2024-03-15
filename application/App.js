
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import RegisterPage from './pages/RegisterPage';
import LoginPage from './pages/LoginPage';
import Menu from './pages/Menu'
import StartDriving from './pages/StartDriving'
import StatisticsPage from './pages/StatisticsPage'
import Camera from './pages/Camera'
import 'react-native-gesture-handler';

const Stack = createStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
    <Stack.Navigator initialRouteName="Login">
      <Stack.Screen name="Login" component={LoginPage} options={{ headerShown: false }} />
      <Stack.Screen name="Register" component={RegisterPage} options={{ headerShown: false }} />
      <Stack.Screen name="Menu" component={Menu} options={{ headerShown: false }} />
      <Stack.Screen name="StartDriving" component={StartDriving} options={{ headerShown: false }} />
      <Stack.Screen name="StatisticsPage" component={StatisticsPage} options={{ headerShown: false }} />
      <Stack.Screen name="Camera" component={Camera} options={{ headerShown: false }} />
    </Stack.Navigator>
  </NavigationContainer>
  );
}
