import React, { Component } from "react";
import CreateDrinkPage from "./CreateDrinkPage";
import Maintenance from "./Maintenance";
import settings from "./SettingsPage";
import menu from "./MenuPage";
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



export default class HomePage extends Component {
  constructor(props) {
    super(props);
  }

  // HAVE IT START COMPILING ALL THE DRINKS IT CAN WHILE THE USER IS IN THE HOMEPAGE IF THE MENU PAGE TAKES TO LONG TO POPULATE
  // async componentDidMount() {
  //   fetch("/api/LoadDrinks").then((response) => response.json())
  // }


  //  NEXT TIME ON DRAGON BALL Z NEED TO ROUTE THE BUTTONS TO THE CORRECT PATH AND HAVE IT DISPLAY WHAT IT NEEDS TO DISPLAY


  renderHomePage() {
    return (
      <Grid container spacing={1}>
        <Grid item xs={12} align="center">
          <Typography component="h4" variant="h4">
            BBC
          </Typography>
        </Grid>

        <Grid item xs={12} align="center">
          <Button color="secondary" variant="contained" to="/CreateDrinkPage" component={Link}>
            Create Drink
          </Button>
        </Grid>

        <Grid item xs={12} align="center">
          <Button color="secondary" variant="contained" to="/settings" component={Link}>
            Settings
          </Button>
        </Grid>

        <Grid item xs={12} align="center">
          <Button color="secondary" variant="contained" to="/MenuPage" component={Link}>
            Menu
          </Button>
        </Grid>

        <Grid item xs={12} align="center">
          <Button color="secondary" variant="contained" to="/Maintance" component={Link}>
            Survey
          </Button>
        </Grid>

        <Grid item xs={12} align="center">
          <Button color="secondary" variant="contained" to="/Maintenance" component={Link}>
            Maintenance
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
            path="/"
            render={() => { return this.renderHomePage() }}
          />
      
        </Switch>
      </Router>
    );
  }
}
  




