import React, { Component } from 'react';
import axios from 'axios';

//import ReactBootstrap, {Jumbotron, Button, Col, Grid, Panel, FormGroup} from 'react-bootstrap'
import Button from 'react-bootstrap/Button'
import ButtonToolbar from 'react-bootstrap/ButtonToolbar'

var Querystring = require('querystring');

class App extends Component {
  
	state = {
		token: "",
		st: "",
		lessons: [],
		txt: "",
		match: ""
	};

	// Ready to send the requests
	componentDidMount() {
		
		this.authenticate();
		//this.setLesson("Inferno I 1-30");
		//this.getHelpFile();
		//this.match("nel mezzo del cammin di nostra vita");
		//this.getNextPrompt();		
		//this.getBackPrompt();
	}
	
	// Authenticate
	authenticate() {
	  
		const data = {
			//grant_type: USER_GRANT_TYPE,
			//client_id: CLIENT_ID,
			//client_secret: CLIENT_SECRET,
			//scope: SCOPE_INT,
			username: 'poetry',
			password: 'poetry'
		};

		/*const params = {
	  
			headers: { 
				'Access-Control-Allow-Origin':'*', 
				'Access-Control-Allow-Headers': 'Content-Type,Authorization', 
				'Access-Control-Allow-Methods':'GET,PUT,POST,DELETE,OPTIONS' 
			}
		}*/
	  
		axios.post('http://127.0.0.1:8000/dante/api-token-auth/', Querystring.stringify(data))   
		.then(response => {
			console.log('api-token-auth ' + response.data.token);
			this.setState({ token:response.data.token}, function() {
				this.init();
			});
			//this.setState({ lessons: '{"id":"1","title":"a","description":"des"}' });
		})   
		.catch((error) => {
			console.log('error ' + error);   
		});
	}

	
	// Initialize
	init() {
	  
	    const AuthStr = 'Token '.concat(this.state.token);
		
		axios.get('http://127.0.0.1:8000/dante/init/', { headers: { Authorization: AuthStr } })
		.then(response => {
			// If request is good...
			console.log('init: ' + response.data.state.namespace);
			this.setState({st: response.data.state}, function() {
				this.getLessons();
			});		
		})
		.catch((error) => {
			console.log('error ' + error);
		});
	}

	// Get Lessons
	getLessons() {
	  
		const AuthStr = 'Token '.concat(this.state.token);
		
		axios.post('http://127.0.0.1:8000/dante/message/', {"message":["get_available_lessons"], "state":this.state.st}, { headers: { Authorization: AuthStr } })
		.then(response => {
			// If request is good...
			console.log('lessons: ' + response.data.lessons);	
			this.setState({lessons: response.data.lessons}, function() {
				this.setLesson(this.state.lessons[0]);
			});		
		})
		.catch((error) => {
			console.log('error ' + error);
		});
	}
	
	// Set Lesson
	setLesson(lesson) {
	  
		const AuthStr = 'Token '.concat(this.state.token); 
	
		console.log('lesson: ' + lesson);
	
		axios.post('http://127.0.0.1:8000/dante/message/', {"message":["set_lesson_by_name", lesson], "state":this.state.st}, { headers: { Authorization: AuthStr } })
		.then(response => {
			// If request is good...
			console.log('txt: ' + response.data.text);
			this.setState({txt: response.data.text});			
		})
		.catch((error) => {
			console.log('error ' + error);
		});
	}

	// Get help file
	getHelpFile() {
	  
		const AuthStr = 'Token '.concat(this.state.token);
		
		axios.post('http://127.0.0.1:8000/dante/message/', {"message":["help_file"], "state":this.state.st}, { headers: { Authorization: AuthStr } })
		.then(response => {
			// If request is good...
			// TODO: Find the correct field
			//console.log('help file: ' + response.data.);			
		})
		.catch((error) => {
			console.log('error ' + error);
		});
	}
	
	// Match sentence
	match(sentence) {
	  
		const AuthStr = 'Token '.concat(this.state.token);
		
		console.log('sentence: ' + sentence);
	
		axios.post('http://127.0.0.1:8000/dante/message/', {"message":["match", sentence], "state":this.state.st}, { headers: { Authorization: AuthStr } })
		.then(response => {
			// If request is good...
			console.log('match: ' + response.data.match);
			this.setState({match: response.data.match});			
		})
		.catch((error) => {
			console.log('error ' + error);
		});
	}

	// Next
	getNextPrompt() {
	  
		console.log('this.state.token: ' + this.state.token);
		
	}

	// Back
	getBackPrompt() {
	  
		const AuthStr = 'Token '.concat(this.state.token);
			
		axios.post('http://127.0.0.1:8000/dante/message/', {"message":["back"], "state":this.state.st}, { headers: { Authorization: AuthStr } })
		.then(response => {
			// If request is good...
			console.log('text: ' + response.data.text);
			this.setState({text: response.data.text});					
		})
		.catch((error) => {
			console.log('error ' + error);
		});
	}
	
  /*
  getLessons() {
    axios
      .get('http://127.0.0.1:8000/api/')
      .then(res => {
        this.setState({ todos: res.data });
      })
      .catch(err => {
        console.log(err);
      });
  }*/

  
			/*<ButtonToolbar>
				<Button variant="primary" onClick="back()">Back</Button>
				<Button variant="secondary">Next</Button>
			</ButtonToolbar>*/
			
	render() {
		return (
		<div>
			<h3>Init completed</h3>
			<p>
				Token: {this.state.token}
			</p>
			<p> Lessons:
				<select>
					{this.state.lessons.map(lesson => <option key={lesson}>{lesson}</option>)}
				</select>
			</p>
			<p>
				Prompt: {this.state.text}
			</p>
			<p>
				{this.state.match}
			</p>
			
			<button onClick={this.getBackPrompt}>Back</button>
			<button onClick={this.getNextPrompt}>Next</button>
				
		</div>
	);
	}
}

export default App;