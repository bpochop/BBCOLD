import React,  { Component } from 'react';
import ConfirmOrder from './ConfirmOrder';
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
  

export default class MenuPage extends Component {
    constructor(props) {
        super(props);
    }
    
    async componentDidMount() {
        fetch("/api/LoadDrinks").then((response) => console.log(response.json()))
    }

    renderMenuPage() {
        return (
          <Grid container spacing={1}>
            <Grid item xs={12} align="center">
              <Typography component="h4" variant="h4">
                BBC
              </Typography>
            </Grid>
    
            <Grid item xs={12} align="center">
              <Button color="secondary" variant="contained" to="/" component={Link}>
                Back
              </Button>
            </Grid>
    
          </Grid>
        );
    }

    render() {
        return (
          <Router>
            <Switch>
              <Route
                exact
                path="/menu"
                render={() => { return this.renderMenuPage() }}
              />
              <Route path="/confirm" component = {ConfirmOrder} />
            </Switch>
          </Router>
        );
      }
    }
      