import React, { useEffect, useState } from "react";
import { Redirect, Route } from "react-router-dom";

const PrivateRoute = ({ component: Component, ...rest }) => {
    const [isLoggedIn, setIsLoggedIn] = useState([]);

    useEffect(() => {
        fetch("/is_logged_in").then((response) =>
            response.json().then((data) => {
                console.log(data.is_logged_in);
                setIsLoggedIn(data.is_logged_in);
            })
        );
    }, []);

    return (
        <Route
            {...rest}
            render={(props) =>
                isLoggedIn ? (
                    <Component {...props} />
                ) : (
                    <Redirect to={{ pathname: "/login", state: { from: props.location } }} />
                )
            }
        />
    );
};

export default PrivateRoute;
