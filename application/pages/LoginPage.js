import {React, useState } from 'react';
import { View, Text, TextInput, Image, StyleSheet, TouchableOpacity ,ScrollView} from 'react-native';
import  {useNavigation ,useRoute} from '@react-navigation/native';
import LoginImage from '../tools/loginandregister.jpg';
import 'react-native-gesture-handler';


export default function LoginPage() {
  const navigation = useNavigation();
  const route = useRoute();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [usernameEmpty, setUsernameEmpty] = useState(false);
  const [passwordEmpty, setPasswordEmpty] = useState(false);
  const [errorInLogin,setErrorInLogin] = useState(false);
  const [errorInConnect,setErrorInConnect] = useState(false);
  var finalSeconds = 0;
  var isDriving = false;
  async function send(){
    if(username.trim() === '' || password.trim() === '' ){
      if (username.trim() === '') 
        setUsernameEmpty(true);
      if (password.trim() === '')
      setPasswordEmpty(true);
    }
    else {
      setUsernameEmpty(false);
      setPasswordEmpty(false);
      const forToken = {
        username: username,
        password: password
      };
      try {
          const response = await fetch('https://6d42-2a02-6680-2102-fe54-656b-b757-38b9-5c8a.ngrok-free.app/api/Login', {
            method: 'post',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(forToken)
            });
          if (response.status === 200) {
            setUsernameEmpty(false);
            setPasswordEmpty(false);
            setPassword("");
            setUsername("");
            setErrorInConnect(false);
            setErrorInLogin(false);
            const token = await response.text();
            navigation.navigate('Menu',{finalSeconds,isDriving,toSend:false,prev:0,token:token,hour:0});

          }else if (response.status === 403){
            setErrorInConnect(false);
            setErrorInLogin(true);
          }else if (response.status === 404){
            setErrorInConnect(true);
          }

      } catch (error) {
        setErrorInConnect(true);
        setUsernameEmpty(false);
        setPasswordEmpty(false);
        setPassword("");
        setUsername("");
      }
    }
  };

  const navigateToRegister = () => {
    navigation.navigate('Register');
  };

  return (
    <>
    <ScrollView contentContainerStyle={styles.scrollContainer}>
      <View style={styles.image}>
        <Image source={LoginImage} style={styles.image} />
      </View>
      <View style={styles.container}>
        <Text style={styles.login}>Login</Text>
        <Text style={styles.label}>Username</Text>
        <TextInput
          style={styles.input}
          placeholder='Type your username'
          value={username}
          onChangeText={(text) => {
            setUsername(text);
            setUsernameEmpty(false);
          }}
        />
        {usernameEmpty && <Text style={styles.error}> Username cannot be empty! </Text>}
        <Text style={styles.label}>Password</Text>
        <TextInput
          style={styles.input}
          placeholder='Type your password'
          secureTextEntry={true}
          value={password}
          onChangeText={(text) => {
            setPassword(text);
            setPasswordEmpty(false); 
          }}
        />
        {passwordEmpty && <Text style={styles.error}>Password cannot be empty!</Text>}
        <TouchableOpacity style={styles.button} onPress={send}>
          <Text style={styles.buttonText}>Login</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.registerLink} onPress={navigateToRegister}>
          <Text style={styles.registerText}>Not registered? Click here to register</Text>
        </TouchableOpacity>
        {errorInLogin &&!errorInConnect&& <Text style={styles.error}>This username or password are incorrect</Text>}
        {errorInConnect && <Text style={styles.error}>Error connecting to the server</Text>}
      </View>
      </ScrollView>
    </>
  );
}
const styles = StyleSheet.create({
  scrollContainer: {
    flexGrow: 1,
    paddingBottom: 20,
  },
  container: {
    justifyContent: 'center',
    paddingHorizontal: 20,
    backgroundColor: '#fff',
    paddingVertical: 20, 
  },
  image: {
    width: '100%',
    height: 200,
    top: 0,
    left: 0,
    right:0
  },
  login: {
    marginTop:20,
    marginBottom:20,
    fontSize: 50,
    fontWeight: 'bold',
    textAlign: 'center',
    color: '#333',
  },
  label: {
    fontSize: 20,
    marginBottom: 8,
    marginTop:8,
    color: '#333',
  },
  error: {
    fontSize: 16,
    marginBottom: 8,
    marginTop: 8,
    color: 'red',
    textAlign: 'center',
  },
  
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 8,
    paddingHorizontal: 16,
    paddingVertical: 12,
    marginBottom: 20,
    fontSize: 16,
    backgroundColor: '#fff',
  },
  button: {
    backgroundColor: '#4CAF50',
    paddingVertical: 14,
    borderRadius: 8,
  },
  buttonText: {
    color: '#fff',
    fontSize: 18,
    textAlign: 'center',
    fontWeight: 'bold',
  },
  registerLink: {
    marginTop: 20,
    alignItems: 'center',
  },
  registerText: {
    fontSize: 16,
    color: '#3498db',
  },
});
