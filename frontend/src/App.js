import React from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import PrivateRoute from "./routes/PrivateRoute";
import Home from "./components/home/Home";
import Login from "./components/login/Login";
// Docker: proxy: "http://host.docker.internal:8080"

function App() {
    return (
        <Router>
            <Switch>
                <PrivateRoute exact path="/" component={Home} />
                <Route exact path="/login" component={Login} />
            </Switch>
        </Router>
    );
}
export default App;
