import { useState } from 'react';


export function useInput({
  placeholder = '',
  id = 'NoID',
  type = 'text',
  supportingText = null,
  required = null,
  minlength = -1,
  maxlength = -1,
  func = () => {}
  }) {

  const [value, setValue] = useState(null);

  const input = (
    <md-outlined-text-field
    type={type}
    value={value}
    label={placeholder} 
    id={id}
    minlength={minlength}
    maxlength={maxlength}
    required={required}
    supporting-text={supportingText}
    onKeyPress={() => {func()}}
    onInput={e => setValue(e.target.value)}
    >
    </md-outlined-text-field>
  );

  return [value, input];
}