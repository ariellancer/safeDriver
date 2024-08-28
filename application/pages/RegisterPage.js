import {React, useState } from 'react';
import { View, Text, TextInput, Image, StyleSheet, TouchableOpacity ,ScrollView} from 'react-native';
import  {useNavigation } from '@react-navigation/native';

import 'react-native-gesture-handler';
import RegisterImage from '../tools/loginandregister.jpg';

export default function RegisterPage() {
  const navigation = useNavigation();
  const [firstname, setFirstname] = useState('');
  const [lastname, setLastname] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [repeatPassword, setRepeatPassword] = useState('');
  const [ifFieldEmpty, setIfFieldEmpty] = useState(false);
  const [passwordLegal, setPasswordLegal] = useState(true);
  const [notSamePassword, setNotSamePassword] = useState(false);
  const [isExists, setIsExists] = useState(false);
  const [errorInConnect,setErrorInConnect] = useState(false);
  const regex =/^(?=.*[a-zA-Z]).{8,}$/
  const navigateToLogin = ()=>{
    setIfFieldEmpty(false);
    setPasswordLegal(true);
    setNotSamePassword(false);
    setFirstname('');
    setLastname('');
    setUsername('');
    setPassword('');
    setRepeatPassword('');
    navigation.navigate('Login');
  } 
  async function handleRegister(){
    if(firstname.trim() === '' || lastname.trim() === '' || username.trim() === '' || password.trim() === '' || repeatPassword.trim() === '')
      {
        setIfFieldEmpty(true);
      }
    else{ 
      setIfFieldEmpty(false);
      if (regex.test(password))
      {
        setPasswordLegal(true)
        if (password.trim() ===  repeatPassword.trim()){
          setNotSamePassword(false);
          const newUser = {
            firstname: firstname,
            lastname: lastname,
            username: username,
            password: password};
       try{
                const response = await fetch('https://d35c-2a05-bb80-7-83c4-8c69-3c08-fe52-a2c1.ngrok-free.app/api/Register', {
                'method': 'post',
                'headers':{
                    'Content-Type': 'application/json',
                },
                'body': JSON.stringify(newUser)
            })
         if(response.status === 200){
            navigateToLogin();
         }else if(response.status === 403) {
            setIsExists(true);
            setIfFieldEmpty(false);
            setErrorInConnect(false);
         }else if(response.status === 404) {
            setErrorInConnect(true);
            setIsExists(false);
         }

      }catch(error){
            console.log(error)
            setErrorInConnect(true);
            setIsExists(false);
          }
        }  
        else {
          setNotSamePassword(true);
        }
      }else{
        setPasswordLegal(false);
      }
    }   
  };

  return (
    <>
    <ScrollView contentContainerStyle={styles.scrollContainer}>
      <View style={styles.image}>
        <Image source={RegisterImage} style={styles.image} />
      </View>
      <View style={styles.container}>
        <Text style={styles.register}>Register</Text>
        <TextInput
          style={styles.input}
          placeholder='First Name'
          value={firstname}
          onChangeText={(text) => {
            setFirstname(text);
          }}
        />
        <TextInput
          style={styles.input}
          placeholder='Last Name'
          value={lastname}
          onChangeText={(text) => {
            setLastname(text);
          }}
        />
        <TextInput
          style={styles.input}
          placeholder='Username'
          value={username}
          onChangeText={(text) => {
            setUsername(text);
          }}
        />
        <TextInput
          style={styles.input}
          placeholder='Password'
          secureTextEntry={true}
          value={password}
          onChangeText={(text) => {
            setPassword(text);
          }}
        />
        <TextInput
          style={styles.input}
          placeholder='Repeat Password'
          secureTextEntry={true}
          value={repeatPassword}
          onChangeText={(text) => {
            setRepeatPassword(text);
          }}
        />
        {ifFieldEmpty && <Text style={styles.error}>One or more of the fields are empty!</Text>}
        {!passwordLegal && <Text style={styles.error}>Password must be at least 8 characters long and contain at least one letter.</Text>}
        {notSamePassword && (!ifFieldEmpty) && passwordLegal &&<Text style={styles.error}>The Passwords are not equals!</Text>}
        <TouchableOpacity style={styles.button} onPress={handleRegister}>
          <Text style={styles.buttonText}>Register</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.registerLink} onPress={navigateToLogin}>
          <Text style={styles.registerText}>Already registered? Click here to login</Text>
        </TouchableOpacity>
        {isExists  && <Text style={styles.error}>Username exists, try another Username</Text>}
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
    right: 0,
  },
  error: {
    fontSize: 20,
    marginBottom: 10,
    marginTop:10,
    color: 'red',
    textAlign: 'center',
  },
  register: {
    fontSize: 50,
    fontWeight: 'bold',
    textAlign: 'center',
    color: '#333',
    marginTop: 20,
    marginBottom:20
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
