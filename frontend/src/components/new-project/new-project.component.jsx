import React from 'react'
import {Typography} from "@material-ui/core";

import './new-project.component.css'
import axios from 'axios';

class NewProject extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            projectName: '',
            videoFile: null,
            subtitleFile: null
        };

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(event) {
        console.log(event.target.id);
        if (event.target.id === 'projectName') {
            this.setState({projectName: event.target.value})
            console.log(this.state.projectName)
        } else if (event.target.id === 'videoFile') {
            this.setState({
                videoFile: event.target.files[0],
                loaded: 0
            });
            console.log(this.state.videoFile)

        } else if (event.target.id === 'subtitleFile') {
            this.setState({
                subtitleFile: event.target.files[0],
                loaded: 0
            });
            console.log(this.state.subtitleFile)

        }
    }

    handleSubmit(event) {
        const data = new FormData()
        data.append('project_name', this.state.projectName);
        data.append('video', this.state.videoFile);
        data.append('subtitle', this.state.subtitleFile);
        axios.post("http://127.0.0.1:8000/api/video/", data, {
            // receive two    parameter endpoint url ,form data
        }).then(res => console.log(res.data))

        alert('A name was submitted: ' + this.state.projectName);
        event.preventDefault();
    }

    render() {
        return (
            <div className="new-project">
                <Typography variant="h2" component="h2">
                    New Project
                </Typography>
                {/*<form onSubmit={this.handleSubmit}>*/}
                {/*    <Container maxWidth="sm">*/}
                {/*        <label>*/}
                {/*            Name:*/}
                {/*            <input id="projectName" type="text" value={this.state.projectName}*/}
                {/*                   onChange={this.handleChange}/>*/}
                {/*        </label>*/}
                {/*        <label>*/}
                {/*            Video File*/}
                {/*            <input id="videoFile" type="file" onChange={this.handleChange}/>*/}
                {/*        </label> <label>*/}
                {/*        Subtitle File*/}
                {/*        <input id="subtitleFile" type="file" onChange={this.handleChange}/>*/}
                {/*    </label>*/}
                {/*        <input type="submit" value="Submit"/>*/}
                {/*        <Button*/}
                {/*            variant="contained"*/}
                {/*            component="label"*/}
                {/*        >*/}
                {/*            Upload File*/}
                {/*            <input*/}
                {/*                type="file"*/}
                {/*                style={{ display: "none" }}*/}
                {/*            />*/}
                {/*        </Button>*/}
                {/*    </Container>*/}
                {/*</form>*/}


            </div>
        );
    }

}

export default NewProject