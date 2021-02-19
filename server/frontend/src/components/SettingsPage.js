import React,  { Component } from 'react';
import CreateDrinkPage from "./CreateDrinkPage";
import Maintenance from "./Maintenance";
import settings from "./SettingsPage";
import menupage from "./MenuPage";
import survey from "./Survey"

import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  Redirect,
} from "react-router-dom";
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import TextField from "@material-ui/core/TextField";
import FormHelperText from "@material-ui/core/FormHelperText";
import FormControl from "@material-ui/core/FormControl";
import Radio from "@material-ui/core/Radio";
import RadioGroup from "@material-ui/core/RadioGroup";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import { Menu } from "@material-ui/core";

export default class SettingsPage extends Component {
    constructor(props) {
        super(props);
        console.log("constructor")
        this.state = {
            pump1: '',
            pump2: '',
            pump3: '',
            pump4: '',
            pump5: '',
            pump6: '',
            pump7: '',
            pump8: '',
            
        };
        this.handleChange = this.myChangeHandler.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    myChangeHandler = (event) =>{
        console.log("change handler")
        let p1 = event.target.pump1;
        let p2 = event.target.pump2;
        let p3 = event.target.pump3;
        let p4 = event.target.pump4;
        let p5 = event.target.pump5;
        let p6 = event.target.pump6;
        let p7 = event.target.pump7;
        let p8 = event.target.pump8;

        //send object here bitch
    }

    handleSubmit(event) {
        console.log("submit")
        console.log(event)
    }

    // componentDidMount(){
    //     this.getCurrentSong();
    // }

    getCurrentSong() {
        console.log("fetch")
        fetch("/api/get-pumps")
          .then((response) => response.json())
          .then((data) => {
            console.log(data);
            console.log("end of data")
          });
      }

    renderHomePage() {
        console.log("renderHomePage")
        return (
            <form>
                <p>Enter your name:</p>
                <input
                type='text'
                name='p1'
                onChange={this.myChangeHandler}
                />

                <p>Enter your name:</p>
                <input
                type='text'
                name='p2'
                onChange={this.myChangeHandler}
                />

            <p>Enter your name:</p>
            <input
            type='text'
            name='p3'
            onChange={this.myChangeHandler}
            />

            <p>Enter your name:</p>
            <input
            type='text'
            name='p4'
            onChange={this.myChangeHandler}
            />

            <p>Enter your name:</p>
            <input
            type='text'
            name='p5'
            onChange={this.myChangeHandler}
            />

            <p>Enter your name:</p>
            <input
            type='text'
            name='p6'
            onChange={this.myChangeHandler}
            />

            <p>Enter your name:</p>
            <input
            type='text'
            name='p7'
            onChange={this.myChangeHandler}
            />
            <input type="submit" value="Submit" />

            </form>
        );
    }

    render() {
        console.log("render")
        return (
            <Router>
            <Switch>
                <Route
                exact
                path="/"
                render={() => { return this.renderHomePage() }}
                />
                {/* <Route path="/settings" component = {settings} /> */}
                
            </Switch>
            </Router>
        );
    }
}