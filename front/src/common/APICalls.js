import { API_URL } from '../config';


export let token = localStorage.getItem('Token');
var bearer = 'Bearer ' + token;


export async function APINoBody(endpoint, methodVerb) {
  return await fetch(API_URL + endpoint, {
    method: methodVerb,
    headers: {
      Authorization: bearer,
      Accept: 'application/json'
    },
  });
}


export async function APIBody(endpoint, methodVerb, form) {
  return await fetch(API_URL + endpoint, {
    method: methodVerb,
    body: form,
    headers: {
      Authorization: bearer,
      Accept: 'application/json'
    },
  });
}


export async function APINoAuth(endpoint, methodVerb, form) {
  return await fetch(API_URL + endpoint, {
    method: methodVerb,
    headers: { 'Content-Type': 'application/json' },
    body: form
  })
}