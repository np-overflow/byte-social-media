import React from "react"

import Masonry from "react-masonry-component"
import AdminFeedCard from "./AdminFeedCard"
import { requestPosts } from "../common/card/media_card/feed/feed_comm"
import FeedFilterControls from "./FeedFilterControls";

const DISPLAY_APPROVED = "approved"
const DISPLAY_ALL = "all"
const DISPLAY_REJECTED = "rejected"

export default class AdminFeed extends React.Component {
    constructor(props) {
        super(props)

        this.state = {
            ws: null,
            posts: [],
            displayPosts: [],
            displayType: DISPLAY_ALL,
        }

        this.postHandler = this.postHandler.bind(this)
        this.changeFilterType = this.changeFilterType.bind(this)
        this.changeFilterToAll = this.changeFilterToAll.bind(this)
        this.changeFilterToApproved = this.changeFilterToApproved.bind(this)
        this.changeFilterToRejected = this.changeFilterToRejected.bind(this)
    }

    postHandler(postJson) {
        this.setState(prevState => {
            let newState = {
                posts: prevState.posts.concat(postJson)
            }

            const adminFeedCardProps = {
                key: postJson["id"],
                cardJson: postJson,
                websocket: prevState.ws,
            }

            switch (prevState.displayType) {
                case DISPLAY_ALL:
                    newState.displayPosts = prevState.displayPosts.concat(
                        <AdminFeedCard {...adminFeedCardProps} />
                    )
                    break
                case DISPLAY_APPROVED:
                    if (postJson["isApproved"]) {
                        newState.displayPosts = prevState.displayPosts.concat(
                            <AdminFeedCard {...adminFeedCardProps} />
                        )
                    }
                    break
                case DISPLAY_REJECTED:
                    if (postJson["isApproved"] === false) {
                        newState.displayPosts = prevState.displayPosts.concat(
                            <AdminFeedCard {...adminFeedCardProps} />
                        )
                    }
                    break
            }

            return newState
        })
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

    componentWillUnmount() {
        this.state.ws.close()
    }

    changeFilterType(newType) {
        if (this.state.displayType === newType) {
            return
        }

        this.setState(prevState => {
            let filterFn;
            switch (newType) {
                case DISPLAY_ALL:
                    filterFn = post => true
                    break
                case DISPLAY_APPROVED:
                    filterFn = post => post["isApproved"]
                    break
                case DISPLAY_REJECTED:
                    filterFn = post => !post["isApproved"]
                    break
            }

            return {
                displayPosts: prevState.posts
                    .filter(filterFn)
                    .map(post => <AdminFeedCard key={post["id"]}
                                                websocket={prevState.ws}
                                                cardJson={post} />),
                displayType: newType
            }
        })
    }

    changeFilterToAll(event) { this.changeFilterType(DISPLAY_ALL) }
    changeFilterToApproved(event) { this.changeFilterType(DISPLAY_APPROVED) }
    changeFilterToRejected(event) { this.changeFilterType(DISPLAY_REJECTED) }

    render() {
        return (
            <div>
                <FeedFilterControls allHandler={this.changeFilterToAll}
                                    approvedHandler={this.changeFilterToApproved}
                                    rejectedHandler={this.changeFilterToRejected} />
                <Masonry {...this.props.masonryProps}>
                    {this.state.displayPosts}
                </Masonry>
            </div>
        )
    }
}