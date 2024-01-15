import React from 'react';
import { APIBody, APINoBody } from './common/APICalls';
import { sha256 } from './LoginRegisterComponent';


async function deleteAccount() {
  try {
    const response = await APINoBody('/users/', 'DELETE')

    if (response.ok) {logOut()} 
  }
  catch(err) {return} 
}


async function logOut() {
  const date = new Date();
  date.setTime(date.getTime() - 60000 * 99999999);
  localStorage.setItem('Expiration', date);
  window.location.reload();
}


async function updateProfile(endpoint, newData, isPassword) {
  try {
    if (isPassword & newData) {
      newData = await sha256(newData);
    }
    if (newData) {
      var textResponse = await APIBody(endpoint, 'POST', JSON.stringify({ txt: newData }))
    }
    if (textResponse) {alert(isPassword ? 'Password updated' : 'E-mail updated');}
    else {
      return alert('Failed to edit profile');
    }
  }
  catch(err) {return}
}


export default function MainFeed() {
  
let email = localStorage.getItem('E-mail');

  return (
    <>
      <md-filled-button id='navButtons' onClick={() => {logOut()}}>Log out</md-filled-button>
      <br></br>
      <br></br>
      <md-outlined-text-field
        type={'email'}
        label={'Change E-mail'}
        minlength={8}
        maxlength={50}
        id={'EmailChanger'}
        value={email}
        >
        <md-icon-button slot='trailing-icon' onClick={(e) => {
            updateProfile('/users/email', document.getElementById('EmailChanger').value, false)
          }}
        >
          <md-icon>send</md-icon>
        </md-icon-button>
      </md-outlined-text-field>
      <br></br>
      <br></br>
      <md-outlined-text-field
        type={'password'}
        label={'Change password'}
        minlength={8}
        maxlength={30}
        id={'PasswordChanger'}
      >
        <md-icon-button slot='trailing-icon' onClick={(e) => {
            updateProfile('/users/password', document.getElementById('PasswordChanger').value, true)
          }}
        >
          <md-icon>send</md-icon>
        </md-icon-button>
      </md-outlined-text-field>
      <br></br>
      <br></br>
      <md-text-button id='navButtons' onClick={() => {deleteAccount()}}>Delete account</md-text-button>
    </>
  )
}
