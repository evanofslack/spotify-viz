import React, { useEffect, useState } from 'react';
import { Redirect, Route } from 'react-router-dom';

const PrivateRoute = ({ component: Component, ...rest }) => {
  const [isLoggedIn, setIsLoggedIn] = useState([]);

  useEffect(() => {
    fetch('/home').then(response =>
      response.json().then(data => {
        console.log(data.isLoggedIn);
        setIsLoggedIn(data.isLoggedIn);
      })
    );
  }, []);

  return (
    <Route
      {...rest}
      render={props =>
        isLoggedIn ? (
          <Component {...props} />
        ) : (
          <Redirect
            to={{ pathname: '/login', state: { from: props.location } }}
          />
        )
      }
    />
  );
};

export default PrivateRoute;
