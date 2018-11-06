import React from "react"
import axios from "axios"

import { API_ENDPOINT_HASHTAGS } from "../settings"

export default class HashtagTitle extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            hashtags: ""
        }
    }

    setHashtags(hashtags) {
        this.setState({
            hashtags: Array.join(hashtags, " ")
        })
    }

    componentDidMount() {
        axios.get(API_ENDPOINT_HASHTAGS)
            .then(response => {
                this.setHashtags(response.data)
            })
    }

    render() {
        return <h1 className={this.props.className}>See your post here! Hashtag {this.state.hashtags}</h1>
    }
}