import React from "react"
import axios from "axios"

import { API_ENDPOINT_HASHTAGS } from "../settings"

export default class HashtagTitle extends React.Component {
    render() {
        return <h1 className={this.props.className}>See your post here! Send your posts through telegram to bytehackz_bot</h1>
    }
}