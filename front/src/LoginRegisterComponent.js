import { useInput } from './common/elemFuncs';
import { APINoAuth } from './common/APICalls';
import React, { useState, useEffect } from 'react';


export async function sha256(str) {
  const encoder = new TextEncoder();
  const data = encoder.encode(str);

  const hashBuffer = await crypto.subtle.digest('SHA-256', data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));

  const hashHex = hashArray.map(byte => byte.toString(16).padStart(2, '0')).join('');
  
  return hashHex;
}


export default function LoginRegisterComponent() {
  const [showRegister, setShowRegister] = useState(false)

  const [email, emailInput] = useInput({ type: 'email', placeholder: 'E-mail', supportingText: null, required: true, minlength: 8, maxlength: 50, id: 'startPageFields'});
  const [firstName, firstNameInput] = useInput({ type: 'text', placeholder: 'First name', supportingText: null, required: true, minlength: 2, maxlength: 50, id: 'startPageFields'});
  const [lastName, lastNameInput] = useInput({ type: 'text', placeholder: 'Last name', supportingText: null, required: true, minlength: 2, maxlength: 50, id: 'startPageFields'});
  const [password, passwordInput] = useInput({ type: 'password', placeholder: 'Password', supportingText: 'Must be at least 8 characters', required: true, minlength: 8, maxlength: 30, id: 'startPageFields'});
  const [password1, password1Input] = useInput({ type: 'password', placeholder: 'Repeat password', supportingText: 'Must match the above password', required: true, minlength: 8, maxlength: 30, id: 'startPageFields'});


  async function sendData() {

    try{
      
      const hashedPassword = await sha256(password);
      if (showRegister){

        if (password !== password1) {
          alert('Passwords do not match.');
          return;
        }

        const body = JSON.stringify({
          email: email,
          password: hashedPassword,
          first_name: firstName,
          last_name: lastName,
        })

        const response = await APINoAuth('/users/register', 'POST', body)
      
        if (response.ok) {
          setShowRegister(false)
        } else {
          alert('Invalid register data, please try again.');
        }
      }
        
      else {
        if (!email || !password) {return}

        const body = JSON.stringify({
          email: email,
          password: hashedPassword
        })
      
        const response = await APINoAuth('/users/', 'POST', body)

        if (response.ok) {
          const json = await response.json();
          const data = JSON.parse(json);
          const date = new Date();
          date.setTime(date.getTime() + 600 * 1000000);
          localStorage.setItem('Verified', data.is_verified);
          localStorage.setItem('E-mail', data.email);
          localStorage.setItem('Token', data.token);
          localStorage.setItem('UserID', data.user_id);
          localStorage.setItem('Expiration', date);
          window.location.reload(false);
        }
        else {
          alert('Invalid login data, please try again.')
        }
      }

      const urlWithoutParams = window.location.href.split('?')[0];
      window.history.pushState({}, '', urlWithoutParams);
      }

    catch(err) {return}
  }

  useEffect(() => {
    function handleKeyDown(e) {

      if (e.keyCode === 13) {
        e.preventDefault();
        sendData();
      }
    }
    document.addEventListener('keydown', handleKeyDown);
    return () => {
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [email, firstName, lastName, password, password1]);

  return (
    <div className='text-center col-lg-4 container py-3 rounded-3 borders-color centerLoginRegister'>
      <form>

        <div className='col-sm-10 mx-auto my-3'>{emailInput}</div>
        {showRegister ? 
            <>
            <div className='col-sm-10 mx-auto my-3'>{firstNameInput}</div>
            <div className='col-sm-10 mx-auto my-3'>{lastNameInput}</div>
            </> 
        : 
            null
        }
        <div className='col-sm-10 mx-auto my-3'>{passwordInput}</div>
        
        {showRegister ? 
            <div className='col-sm-10 mx-auto my-3'>{password1Input}</div>
        :
            null
        }
      </form>

      <div className='d-flex align-items-center justify-content-evenly'>

        <md-text-button onClick={() => {setShowRegister(!showRegister)}}>
          {showRegister ? 'Already have an account?' : "Don't have an account?"}
        </md-text-button>

        <md-filled-button onClick={() => {sendData()}}>
          {showRegister ? 'Submit' : 'Enter'}
        </md-filled-button>
      </div>
    </div>
  );
}

