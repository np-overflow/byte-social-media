import React from "react"

import Masonry from "react-masonry-component"

import { API_SOCKET_ENDPOINT_POSTS } from "../settings"

export default class Feed extends React.Component {
    constructor(props) {
        super(props)

        this.state = {
            ws: null,
            posts: []
        }
    }

    createWebSocket() {
        console.log(API_SOCKET_ENDPOINT_POSTS)
        const ws = new WebSocket(API_SOCKET_ENDPOINT_POSTS)
        ws.addEventListener("message", event => {
            console.log(event.data)
        })
    }

    componentDidMount() {
        this.setState({
            ws: this.createWebSocket()
        })
    }

    render() {
        return (
            <Masonry {...this.props.masonryProps}>
            </Masonry>
        );
    }
}