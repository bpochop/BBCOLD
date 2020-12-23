import React,  { Component } from 'react';
import { Grid, Button, ButtonGroup, Typography} from '@material-ui/core'
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
import { Grid, Typography } from '@material-ui/core';




export default class HomePage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            roomCode:null, 
        };
    }

    //usually dont need async but we doing a asynchronous function
    async componentDidMount(){
        fetch('/api/user-in-room')
        .then((response) => response.json())
        .then((data) => {
            this.setState({
                roomCode: data.code
            });
        });
    }

    renderHomePage(){
        reurn (
            <Grid container spacing = {3}>
                <Grid item xs = {2} align = "center">
                    <Typography variant = "h3" compact="h3">WELCOME TO YOUR BBC</Typography>
                </Grid>

                <Grid item xs = {2} align = "center">
                    <ButtonGroup disableElevation variant="contained" color="primary">
                        <Button color ="primary" to ="/join" component={Link}>Join a Room</Button>
                        <Button color ="secondary" to ="/create" component={Link}>Create a Room</Button>
                    </ButtonGroup>    
                </Grid>
            </Grid>
        );
    }
    
    render(){
        return (
            <Router>
                <Switch>
                    <Route exact path = '/' render={() => {
                        return this.state.roomCode ? (<Redirect to={`/room/${this.state.roomCode}`}/>) : this.renderHomePage
                    }}/> 
                   

                    <Route path='/Menu' component={MenuPage}/>
                    <Route path='/create' component= {CreateDrinkPage}/>
                    <Route path = '/settings' component = {SettingsPage}/>
                    <Route path = "/room/:roomCode" component = {Room} />
                    
                </Switch>

            </Router>
        );
    }
}