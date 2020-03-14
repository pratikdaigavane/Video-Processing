import React from 'react'
import {Grid} from "@material-ui/core";
import NewProject from "../new-project/new-project.component";
import MyProjects from "../my-projects/my-projects.component";

class Home extends React.Component {
    render() {
        return (
            <Grid
                container
                direction="row"
                justify="center"
                alignItems="flex-start"
            >

                <Grid item xs={12} sm={6}>
                    <NewProject/>

                </Grid>
                <Grid item xs={12} sm={6}>
                    <MyProjects/>
                </Grid>

            </Grid>
        )
    }
}

export default Home