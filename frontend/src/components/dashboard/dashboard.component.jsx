import React from 'react'
import queryString from 'query-string'
import axios from "axios";
import {Card, CardContent, Grid, Typography} from "@material-ui/core";
import Paper from "@material-ui/core/Paper";
import './dashboard.styles.css'
import Skeleton from '@material-ui/lab/Skeleton';
import VideoPlayer from "../video-player/video-player.component";
import AudioPlayer from "react-h5-audio-player";
import 'react-h5-audio-player/lib/styles.css';
import CardActions from "@material-ui/core/CardActions";
import Button from "@material-ui/core/Button";

class Dashboard extends React.Component {
    constructor() {
        super();
        this.state = {
            current_count: 0,
            total_count: 0,
            project_name: '',
            chunks: []
        }
        let apiLoop

    }

    componentDidMount() {
        const values = queryString.parse(this.props.location.search);
        this.setState({
            total_count: values.totalChunks,
            project_name: values.projectName
        });
        this.apiLoop = setInterval(() => {
            axios.get(`${process.env.REACT_APP_API_URL}/api/video/${values.id}`)
                .then((res) => {
                    console.log(res.data);
                    this.setState({current_count: res.data.count, chunks: res.data.results})
                })
                .catch(() => alert('server offline'));
            console.log(this.state.current_count);
            console.log(this.state.total_count);
            if (this.state.current_count == this.state.total_count) clearInterval(this.apiLoop)


        }, 1000)


    }

    componentWillUnmount() {
        clearInterval(this.apiLoop)

    }

    render() {
        return (
            <div className="dashboard">

                <Grid container spacing={3} direction="row"
                      justify="flex-end"
                      alignItems="flex-start"


                >
                    <Grid item className="hello" xs={12}>

                        <Grid container
                             

                        >
                            <Grid item xs={12} sm={6}>
                                <h1>{this.state.project_name}</h1>
                                <p>Project ID: 13577c62-dfee-47e4-a637-690fbc4026cf</p>
                            </Grid>
                            <Grid item xs={12} sm={6}>
                                {this.state.current_count
                                    ? <h1>Total Chunks: {this.state.current_count} / {this.state.total_count}</h1>
                                    : <div>
                                        <Skeleton variant="text"/>
                                        <Skeleton variant="text"/>
                                        <Skeleton variant="text"/>
                                        <Skeleton variant="text"/>
                                    </div>
                                }

                            </Grid>
                        </Grid>

                    </Grid>
                    <Grid item xs={12} sm={3}>
                        <Paper>xs=12 sm=6</Paper>
                    </Grid>
                    <Grid item xs={12} sm={9} id="videoCard">
                        {
                            this.state.chunks.map((chunk) => {
                                const videoJsOptions = {
                                    autoplay: false,
                                    controls: true,
                                    preload: 'metadata',
                                    sources: [{
                                        src: chunk.video_chunk,
                                        type: 'video/mp4'
                                    }],
                                    width: 350,
                                };
                                return (
                                    <Card key={chunk.chunk_no} className="root">
                                        <VideoPlayer {...videoJsOptions} />
                                        <CardContent>
                                            <Typography variant="h5">
                                                Chunk No: {chunk.chunk_no}
                                            </Typography>
                                            <Typography variant="subtitle1">
                                                Start Time: {chunk.start_time}
                                            </Typography>
                                            <Typography variant="subtitle1">
                                                End Time: {chunk.end_time}
                                            </Typography>

                                            <AudioPlayer
                                                src={chunk.audio_chunk}
                                                preload='metadata'
                                                showJumpControls={false}
                                            />

                                        </CardContent>
                                        <CardActions>
                                            <Button>
                                                Upload Audio
                                            </Button>
                                        </CardActions>


                                    </Card>
                                )
                            })
                        }


                    </Grid>
                </Grid>


            </div>

        )
    }
}

export default Dashboard
