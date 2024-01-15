import TestComponent from './LoginRegisterComponent';
import MainFeed from './MainFeed';
import Verify from './Verify';


export default function App() {

  const verified = localStorage.getItem('Verified')
  const token = localStorage.getItem('Token');
  const date = new Date(localStorage.getItem('Expiration'));
  let ExpiredToken = true

  if (token) {
    if (date) {
      const currentDate = new Date();
      if (currentDate < date) {
        ExpiredToken = false;
      }
    }
  }

  if (ExpiredToken) {
    return (
      <TestComponent/>
    );
  }
  else {
    if (verified == 1) {
      return (
        <MainFeed/>
      )
    }
    else {
      return (<Verify/>)
    }
  }
}