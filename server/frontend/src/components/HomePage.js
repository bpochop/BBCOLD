import React,  { Component } from 'react';
import MenuPage from "./MenuPage";
import SettingsPage from "./SettingsPage";
import CreateDrinkPage from "./CreateDrinkPage";
import { 
    BrowserRouter as Router, 
    Switch, 
    Route, 
    Link, 
    Redirect 
} from "react-router-dom";



export default class HomePage extends Component {
    constructor(props) {
        super(props);
    }

    render(){
        return (
            <Router>
                <Switch>
                    <Route exact path = '/'> <p>This is the Homepage</p> </Route>
                    <Route path='/Menu' component={MenuPage}/>
                    <Route path='/create' component= {CreateDrinkPage}/>
                    <Route path = '/settings' component = {SettingsPage}/>
                    
                </Switch>

            </Router>
        );
    }
}