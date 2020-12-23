import React, {Component} from "react";
import { render } from "react-dom";
import Homepage from './HomePage';
import ConfirmOrder from './ConfirmOrder';
import CreateDrink from './CreateDrinkPage';
import Menu from './MenuPage';
import Settings from './SettingsPage';
import Survey from './Survey';

export default class App extends Component{
    constructor(props){
        super(props);
    }

    render(){
        return (
            <div className ="center" >
                <Homepage />
            </div>
        );
    }
}

const appDiv = document.getElementById("app")
render(<App />,appDiv);