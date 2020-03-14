import React from 'react'
import {Button, Card, CardActions, CardContent, Typography} from "@material-ui/core";
import './my-projects.component.css'
import axios from 'axios'
import VideoPlayer from "../video-player/video-player.component";
import {Link} from "react-router-dom";


class MyProjects extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            count: 0,
            videoList: []
        };
    }

    componentDidMount() {
        axios.get(`${process.env.REACT_APP_API_URL}/api/video`)
            .then((res) => {
                console.log(res.data)
                this.setState({
                    count: res.data.count,
                    videoList: res.data.results
                })
            })
            .catch(() => alert('server offline'))


    }


    render() {
        return (
            <div className="my-projects">
                <Typography variant="h3" component="h3">
                    My Projects
                </Typography>
                <br/><br/>
                <div id="videoCard">
                    {
                        this.state.videoList.map((singleVideo) => {
                            const videoJsOptions = {
                                autoplay: false,
                                controls: true,
                                preload: 'none',
                                sources: [{
                                    src: singleVideo.video,
                                    type: 'video/mp4'
                                }],
                                width: 350,
                            };
                            return (

                                <Card className="root" key={singleVideo.id}>
                                    <div className="details">
                                        <CardContent className="content">
                                            <Typography component="h5" variant="h5">
                                                {singleVideo.project_name}
                                            </Typography>
                                            <p> Project ID: {singleVideo.id}
                                            </p>
                                        </CardContent>
                                        <div className="controls">
                                            <CardActions>
                                                <Link to={`/dashboard?id=${singleVideo.id}&&projectName=${singleVideo.project_name}&&totalChunks=${singleVideo.total_chunks}`


                                                }
                                                      style={{textDecoration: 'none'}}
                                                >
                                                    <Button>
                                                        Open Project
                                                    </Button>
                                                </Link>
                                            </CardActions>

                                        </div>
                                    </div>
                                    <VideoPlayer {...videoJsOptions} />
                                </Card>
                            )
                        })

                    }
                </div>

            </div>
        );
    }

}

export default MyProjects