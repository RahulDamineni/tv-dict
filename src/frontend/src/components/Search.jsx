import React from 'react';
import { TextField } from '@material-ui/core';
import ResultsCanvas from './Results';

export default class Search extends React.Component {

   constructor(props) {
      super(props);
      this.state = {
        value: '',
        matches: [],
        showMatches: false,
      }
      this.handleChange = this.handleChange.bind(this);
      this.keyPress = this.keyPress.bind(this);

   }

   handleChange(e) {
      this.setState({
          value: e.target.value,
          matches: [],
          showMatches: false
         });
   }

   keyPress(e){
   if(e.keyCode === 13){
      console.log('value', e.target.value);
      this.setState({showMatches: true})
      // put the login here

      fetch('http://localhost:5000/search', {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          // 'Access-Control-Allow-Origin': "*",
        },
        body: JSON.stringify({
          query: this.state.value,
        })
      })
      .then((response) => response.json())
      .then((rjson) => {
        console.log(rjson);
        this.setState({matches: rjson});
      })
      .catch((error) => {
        console.error(error);
      });

    }
   }


   render(){

     let results_canvas;
     if (this.state.showMatches) {
       results_canvas = <ResultsCanvas matches={this.state.matches}/>
     }
      return(
        <div>
          <TextField
              placeholder="Search for words..."
              value={this.state.value}
              onChange={this.handleChange}
              onKeyDown={this.keyPress}
              color="secondary"
              margin="dense"
              size="medium"
              variant="outlined"
              fullWidth={true} />
            {results_canvas}
        </div>
      )
   }
}
