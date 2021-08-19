import React, { useState } from 'react';
import { Button } from '@chakra-ui/react';

function TestBackend() {
  const [message, setMessage] = useState('No message');

  async function getMessage() {
    await fetch('/react').then(response =>
      response.json().then(data => {
        setMessage(data.username);
      })
    );
  }

  return (
    <div>
      <Button onClick={() => getMessage()}>Test Backend</Button>
      <div>{message}</div>
    </div>
  );
}

export default TestBackend;
