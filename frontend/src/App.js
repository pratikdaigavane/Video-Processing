import React from 'react'
import AppBarComponent from "./components/app-bar/app-bar.component";
// import VideoPlayer from "./components/video-player/video-player.component"
import CssBaseline from "@material-ui/core/CssBaseline";
import Home from "./components/home/home.component";
import Dashboard from "./components/dashboard/dashboard.component";
import {Route, Switch} from 'react-router-dom';
import Documentation from "./components/documentation/documentation.component";

import './App.css'
class App extends React.Component {

    //
    render() {
        return (
            <div>
                <CssBaseline/>
                <AppBarComponent/>

                    <Switch
                        atEnter={{ opacity: 0 }}
                        atLeave={{ opacity: 0 }}
                        atActive={{ opacity: 1 }}
                        className="switch-wrapper"
                    >

                    <Route exact path='/' component={Home}/>
                    <Route path='/dashboard' component={Dashboard}/>
                    <Route path='/doc' component={Documentation}/>

                    </Switch>

                {/*<VideoPlayer {...videoJsOptions} />*/}

            </div>
        )
    }
}

export default App
