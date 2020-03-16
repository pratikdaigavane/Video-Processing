import React from 'react'
import {Container, Typography} from "@material-ui/core";

import axios from 'axios';
import FormControl from "@material-ui/core/FormControl";
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button"
import 'react-dropzone-uploader/dist/styles.css'
import Dropzone from 'react-dropzone-uploader'
import Snackbar from "@material-ui/core/Snackbar";
import Alert from "@material-ui/lab/Alert";
import './new-project.component.css'
import {withRouter} from 'react-router-dom'
import LinearProgress from "@material-ui/core/LinearProgress";

class NewProject extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            projectName: '',
            videoFile: null,
            subtitleFile: null,
            open: false,
            redirect: false,
            disabled: false,
            project_id: ''

        };

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleUploadSubmit = this.handleUploadSubmit.bind(this);
        this.handleChangeStatus = this.handleChangeStatus.bind(this);
        this.getUploadParams = this.getUploadParams.bind(this);
        this.closeAlert = this.closeAlert.bind(this);


    };

    getUploadParams({meta}) {
        return 1
    };


    closeAlert() {
        this.setState({open: false});
        this.props.history.push(`/dashboard?id=${this.state.project_id}`)

    }


    handleChangeStatus({meta, file}, status) {
        if (file.type === 'video/mp4') {
            this.setState({videoFile: file})
        } else {
            this.setState({subtitleFile: file})
        }
    };

    handleUploadSubmit(files) {
        console.log(files.map(f => f.meta))
    };

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
        this.setState({disabled: true});
        event.preventDefault();
        const data = new FormData();
        data.append('project_name', this.state.projectName);
        data.append('video', this.state.videoFile);
        data.append('subtitle', this.state.subtitleFile);
        axios.post(`${process.env.REACT_APP_API_URL}/api/video/`, data,)
            .then(res => this.setState({project_id: res.data.id}));
        this.setState({open: true});
    }

    render() {
        return (
            <div className="new-project">
                {
                    this.state.disabled ?
                        <LinearProgress color="secondary"/> :
                        null
                }

                <Typography variant="h3" component="h3" className="heading">
                    New Project
                </Typography>

                <Container className={"uploadForm"}>
                    <FormControl color={"secondary"} fullWidth>
                        <TextField id="projectName" label="Project Name" variant="outlined"
                                   onChange={this.handleChange}/>
                        <h1>Video File</h1>
                        <Dropzone
                            className="fileUploader"
                            onChangeStatus={this.handleChangeStatus}
                            accept="video/mp4"
                            multiple={false}
                            autoUpload={false}
                            maxFiles={1}
                            inputContent="Drag Video or Click to Browse"
                        />
                        <h1>Subtitle File</h1>
                        <Dropzone
                            onChangeStatus={this.handleChangeStatus}
                            accept=".srt"
                            multiple={false}
                            autoUpload={false}
                            maxFiles={1}
                            inputContent="Drag Subtitle or Click to Browse"

                        />
                    </FormControl>
                    <br/><br/><br/>
                    <Button disabled={this.state.disabled}
                            variant="contained"
                            color="primary"
                            onClick={this.handleSubmit}
                            size='large'
                    >
                        Submit
                    </Button>
                </Container>

                <Snackbar open={this.state.open} autoHideDuration={2000} onClose={this.closeAlert}


                >
                    <Alert severity="success">
                        Files Uploaded Successfully
                    </Alert>
                </Snackbar>

            </div>
        );
    }

}

export default withRouter(NewProject)