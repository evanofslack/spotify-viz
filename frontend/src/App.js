import React from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import PrivateRoute from "./routes/PrivateRoute";
import Home from "./components/Home";
import Login from "./components/Login";

function App() {
    return (
        <Router>
            <Switch>
                <Route exact path="/login" component={Login} />
                <PrivateRoute exact path="/" component={Home} />
            </Switch>
        </Router>
    );
}
export default App;
