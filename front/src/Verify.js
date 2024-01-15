import { APIBody } from './common/APICalls';


async function verifyEmail(code) {
  try {
    var response = await APIBody('/users/verify', 'POST', JSON.stringify({ txt: code }))
    if (response.ok) {
      localStorage.setItem('Verified', 1);
      window.location.reload(false);
    }
    else {
      alert('Invalid code, please try again.')
    }
  } 
  catch{return}
}


export default function Verify() {
  return (
    <>
      <md-outlined-text-field
        type={'email'}
        label={'Enter E-mail verification code'}
        minlength={6}
        maxlength={6}
        id={'Verifier'}
      >
        <md-icon-button slot='trailing-icon' onClick={(e) => {
            verifyEmail(document.getElementById('Verifier').value)
          }}
        >
          <md-icon>send</md-icon>
        </md-icon-button>
      </md-outlined-text-field>
    </>
  );
}