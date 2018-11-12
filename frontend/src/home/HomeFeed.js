import React from "react"

import Masonry from "react-masonry-component"
import FeedCard from "../common/card/media_card/feed/FeedCard"
import { requestPosts } from "../common/card/media_card/feed/feed_comm"

export default class HomeFeed extends React.Component {
    constructor(props) {
        super(props)

        this.state = {
            ws: null,
            displayPosts: [],
        }
    }

    componentDidMount() {
        const websocket = new WebSocket(this.props.endpoint)
        this.setState({
            ws: websocket
        })

        websocket.addEventListener("message", event => {
            this.postHandler(JSON.parse(event.data))
        })
        requestPosts(websocket)
    }

    postHandler(postJson) {
        this.setState(prevState => ({
            displayPosts: prevState.displayPosts.concat(
                <FeedCard key={postJson["id"]} cardJson={postJson} />
            ),
        }))
    }

    render() {
        return (
            <Masonry {...this.props.masonryProps}>
                {this.state.displayPosts}
            </Masonry>
        )
    }
}