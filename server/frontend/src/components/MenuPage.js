import React,  { Component } from 'react';
import ConfirmOrder from './ConfirmOrder';
import { 
    BrowserRouter as Router, 
    Switch, 
    Route, 
    Link, 
    Redirect 
} from "react-router-dom";

export default class MenuPage extends Component {
    constructor(props) {
        super(props);
    }

    render(){
        return (
            <Router>
                <Switch>
                    <Route path = '/confirm' Component = {ConfirmOrder} />
                </Switch>
            </Router>
        );
    }
}

