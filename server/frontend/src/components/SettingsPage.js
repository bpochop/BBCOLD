import React,  { Component } from 'react';


export default class SettingsPage extends Component {
    constructor(props) {
        super(props);
    }

    componentDidMount(){
        this.getCurrentSong();
    }

    getCurrentSong() {
        fetch("/api/get-pumps")
          .then((response) => response.json())
          .then((data) => {
            console.log(data);
            console.log("end of data")
          });
      }

    render(){
        return <p>This is the new  my guy</p>
       
    }
}