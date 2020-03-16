import React from 'react'
import queryString from 'query-string'
import axios from "axios";
import {Card, CardContent, Grid, Typography} from "@material-ui/core";
import './dashboard.styles.css'
import Skeleton from '@material-ui/lab/Skeleton';
import VideoPlayer from "../video-player/video-player.component";
import AudioPlayer from 'react-h5-audio-player';
import 'react-h5-audio-player/lib/styles.css';
import Button from "@material-ui/core/Button";
import Dialog from "@material-ui/core/Dialog";
import DialogTitle from "@material-ui/core/DialogTitle";
import DialogContent from "@material-ui/core/DialogContent";
import DialogActions from "@material-ui/core/DialogActions";
import Dropzone from 'react-dropzone-uploader'
import 'react-dropzone-uploader/dist/styles.css'
import LinearProgress from "@material-ui/core/LinearProgress";
import Snackbar from "@material-ui/core/Snackbar";
import Alert from "@material-ui/lab/Alert";

class Dashboard extends React.Component {
    constructor() {
        super();
        this.state = {
            current_count: 0,
            total_count: 0,
            project_name: '',
            chunks: [],
            project_id: '',
            open: false,
            chunk_no: null,
            audioFile: null,
            disabled: false,
            alertOpen: false,
            processed_video: '',
            processed: false
        };

        this.openDialog = (chunk) => {
            this.setState({open: true, chunk_no: chunk, audioFile: null})
        };

        this.handleClose = () => {
            this.setState({open: false})
        };

        this.submitAudio = () => {
            this.setState({disabled: true});
            const data = new FormData();
            data.append('audio_chunk', this.state.audioFile);
            axios.put(`${process.env.REACT_APP_API_URL}/api/video/${this.state.project_id}/${this.state.chunk_no}`, data,)
                .then(res => {
                    this.setState({open: false, disabled: false, alertOpen: true})
                }).catch(
                () => alert("error")
            );
            this.fetchData()
        };

        this.handleChangeStatus = ({meta, file}, status) => {
            this.setState({audioFile: file})
        };

        this.fetchData = () => {
            this.setState({processed: false});
            this.apiLoop = setInterval(() => {
                axios.get(`${process.env.REACT_APP_API_URL}/api/video/${this.state.project_id}`)
                    .then((res) => {
                        console.log(res.data);
                        this.setState({
                            current_count: res.data.chunks.length,
                            chunks: res.data.chunks,
                            total_count: res.data.video_data.total_chunks,
                            project_name: res.data.video_data.project_name
                        });
                        if (res.data.video_data.processed_video === null) {
                            this.setState(
                                {
                                    'processed_video': res.data.video_data.video
                                }
                            )
                        } else {
                            this.setState({'processed_video': res.data.video_data.processed_video})
                        }
                        if (res.data.video_data.status === 'done') {
                            clearInterval(this.apiLoop);
                            this.setState({processed: true})

                        }

                    })
                    .catch(() => alert('server offline'));


            }, 1000);
        }


    }


    componentWillMount() {
        const values = queryString.parse(this.props.location.search);
        this.setState({
            project_id: values.id
        });
        this.fetchData();


    }


    componentWillUnmount() {
        clearInterval(this.apiLoop)

    }

    render() {
        return (
            <div className="dashboard">

                <Grid container spacing={3}
                      alignItems="center"
                >
                    <Grid item className="hello" xs={12}>

                        <Grid container spacing={3} className="chunkInfo">
                            <Grid item xs={12} sm={4} style={{
                                padding: '20px'
                            }}>
                                {
                                    this.state.project_name ?
                                        <div>
                                            <h1>{this.state.project_name}</h1>
                                            <p className="projectId">{this.state.project_id}</p>
                                            {
                                                this.state.processed ?
                                                    <p className="done">DONE
                                                    </p> :
                                                    <p className="processing">PROCESSING</p>
                                            }
                                        </div> :
                                        <div>
                                            <Skeleton variant="text"/>
                                            <Skeleton variant="text"/>
                                            <Skeleton variant="text"/>
                                            <Skeleton variant="text"/>
                                            <Skeleton variant="text"/>
                                            <Skeleton variant="text"/>
                                            <Skeleton width="60%" />
                                            <Skeleton width="60%" />

                                        </div>
                                }

                            </Grid>
                            <Grid item xs={12} sm={4}>
                                {this.state.current_count
                                    ? <div>
                                        <h1>Total Chunks: {this.state.current_count} / {this.state.total_count}</h1>
                                        <Button size="large" variant="contained" color="primary" download
                                                href={this.state.processed_video}>
                                            Download Tutorial
                                        </Button>
                                    </div>
                                    : <div>
                                        <Skeleton variant="text"/>
                                        <Skeleton variant="text"/>
                                        <Skeleton variant="text"/>
                                        <Skeleton variant="text"/>
                                        <Skeleton width="60%" />
                                        <Skeleton width="60%" />
                                    </div>
                                }
                            </Grid>
                            <Grid item xs={12} sm={4}>
                                {this.state.processed ?
                                    <VideoPlayer
                                        autoplay={false}
                                        controls={true}
                                        preload="metadata"
                                        width={400}
                                        sources={[{
                                            src: this.state.processed_video,
                                            type: 'video/mp4'
                                        }]}
                                    /> :
                                    <div>
                                        <Skeleton animation="wave" variant="rect" width={400} height={220}/>
                                    </div>

                                }


                            </Grid>
                        </Grid>

                    </Grid>


                    <Grid item xs={12} id="videoCard">
                        {
                            this.state.chunks.map((chunk) => {
                                const videoJsOptions = {
                                    autoplay: false,
                                    controls: true,
                                    preload: 'none',
                                    sources: [{
                                        src: chunk.video_chunk,
                                        type: 'video/mp4'
                                    }],
                                    width: 350,
                                };
                                return (
                                    <Card key={chunk.chunk_no} className="root">
                                        <CardContent className="content">
                                            <Grid
                                                spacing={2}
                                                container
                                                direction="row"
                                                justify="space-between"
                                                alignItems="center"
                                            > <Grid item xs={12} sm={3}>
                                                <VideoPlayer {...videoJsOptions} />
                                            </Grid>
                                                <Grid item xs={12} sm={3}>
                                                    <Typography component="h5" variant="h5">
                                                        Chunk No: {chunk.chunk_no+1}
                                                    </Typography>
                                                    <AudioPlayer
                                                        src={chunk.audio_chunk}
                                                        preload='none'
                                                        onPlay={e => console.log("onPlay")}
                                                        // other props here
                                                    />


                                                </Grid>
                                                <Grid item xs={12} sm={3}>
                                                    <Typography component="h6" variant="h6">
                                                        {chunk.subtitle}
                                                    </Typography>
                                                    <p>Start Time: {chunk.start_time}</p>
                                                    <p>End Time: {chunk.end_time}</p>
                                                </Grid>
                                                <Grid item xs={12} sm={3}>
                                                    <Button
                                                        variant="outlined" color='primary'
                                                        onClick={() => this.openDialog(chunk.chunk_no)}>
                                                        Change Audio
                                                    </Button>
                                                </Grid>

                                            </Grid>


                                        </CardContent>

                                    </Card>

                                )
                            })
                        }


                        <Dialog
                            onClose={this.handleClose}
                            aria-labelledby="customized-dialog-title"
                            open={this.state.open}>
                            <DialogTitle id="customized-dialog-title" onClose={this.handleClose}>
                                Upload Audio
                            </DialogTitle>
                            {
                                this.state.disabled ?
                                    <LinearProgress color="secondary" disabled/> :
                                    null

                            }
                            <DialogContent className="fileUploader" dividers>
                                <Dropzone
                                    onChangeStatus={this.handleChangeStatus}
                                    accept="audio/mp3"
                                    multiple={false}
                                    autoUpload={false}
                                    maxFiles={1}
                                    inputContent="Drag Audio or Click to Browse"
                                />
                            </DialogContent>
                            <DialogActions>
                                <Button disabled={this.state.disabled} autoFocus onClick={this.submitAudio}
                                        color="primary">
                                    Upload
                                </Button>
                            </DialogActions>
                        </Dialog>

                    </Grid>
                </Grid>

                <Snackbar open={this.state.alertOpen} autoHideDuration={5000} onClose={() => {
                    this.setState({alertOpen: false})
                }}


                >
                    <Alert severity="success">
                        Audio Uploaded Successfully
                    </Alert>
                </Snackbar>
            </div>

        )
    }
}

export default Dashboard
