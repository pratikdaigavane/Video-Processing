import React from "react";
import SwaggerUI from "swagger-ui-react"
import "swagger-ui-react/swagger-ui.css"
import "./documentation.styles.css"

class Documentation extends React.Component {

    render() {
        return (
            <SwaggerUI url="/swagger.json"/>
        )
    }

}

export default Documentation