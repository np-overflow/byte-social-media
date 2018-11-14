import React from "react"

import Masonry from "react-masonry-component"
import AdminFeedCard from "./AdminFeedCard"
import { requestPosts } from "../common/card/media_card/feed/feed_comm"
import FeedFilterControls from "./FeedFilterControls"

const DISPLAY_APPROVED = "approved"
const DISPLAY_UNDECIDED = "undecided"
const DISPLAY_REJECTED = "rejected"

export default class AdminFeed extends React.Component {
    constructor(props) {
        super(props)

        this.state = {
            ws: null,
            posts: [],
            displayPosts: [],
            displayType: DISPLAY_UNDECIDED,
        }

        this.postHandler = this.postHandler.bind(this)
        this.changeFilterType = this.changeFilterType.bind(this)
        this.changeFilterToUndecided = this.changeFilterToUndecided.bind(this)
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
                approvalHandler: this.postApprovalHandlerCreator(postJson["id"]),
                cardJson: postJson,
                websocket: prevState.ws,
            }

            switch (prevState.displayType) {
                case DISPLAY_UNDECIDED:
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

    updatePostStatus(posts, postId, newStatus) {
        const postIndex = posts.find(post => post["id"] === postId)
        // Deep copy the post at the post index
        let newPost = JSON.parse(JSON.stringify(posts[postIndex]))
        newPost["isApproved"] = newStatus

        // Create new posts array with the new post
        let newPosts = posts.slice(0, postIndex)
        newPosts.push(newPost)
        return newPosts.concat(posts.slice(postIndex+1))
    }

    postApprovalHandlerCreator(postId) {
        return isApproved => {
            // Update posts state
            this.setState(prevState => {
                // Find the post in posts
                const postIndex = prevState.posts.findIndex(post => post["id"] === postId)

                // Check if there are any changes
                if (prevState.posts[postIndex]["isApproved"] === isApproved) {
                    return {}
                }

                // Deep copy the post at the post index
                let newPost = JSON.parse(JSON.stringify(prevState.posts[postIndex]))
                newPost["isApproved"] = isApproved

                // Create new posts array with the new posts
                let newPosts = prevState.posts.slice(0, postIndex)
                newPosts.push(newPost)
                newPosts = newPosts.concat(prevState.posts.slice(postIndex+1))

                let newState = {
                    posts: newPosts,
                }

                // Determine of displayPosts needs to be updated
                // Check if the current display complements the approval status
                if (prevState.displayType === DISPLAY_UNDECIDED ||
                        (prevState.displayType === DISPLAY_APPROVED && !isApproved) ||
                        (prevState.displayType === DISPLAY_REJECTED && isApproved)) {
                    // Find the post to remove
                    const removePostIndex = prevState.displayPosts.findIndex(post => post.key === postId.toString())

                    newState.displayPosts = prevState.displayPosts.slice(0, removePostIndex-1)
                    newState.displayPosts = newState.displayPosts.concat(prevState.displayPosts.slice(removePostIndex+1))
                }

                return newState
            })
        }
    }

    changeFilterType(newType) {
        if (this.state.displayType === newType) {
            return
        }

        this.setState(prevState => {
            let filterFn
            switch (newType) {
                case DISPLAY_UNDECIDED:
                    filterFn = post => post["isApproved"] === null
                    break
                case DISPLAY_APPROVED:
                    filterFn = post => post["isApproved"]
                    break
                case DISPLAY_REJECTED:
                    filterFn = post => post["isApproved"] === false
                    break
            }

            return {
                displayPosts: prevState.posts
                    .filter(filterFn)
                    .map(post => <AdminFeedCard key={post["id"]}
                                                approvalHandler={this.postApprovalHandlerCreator(post["id"])}
                                                websocket={prevState.ws}
                                                cardJson={post} />),
                displayType: newType
            }
        })
    }

    changeFilterToUndecided() { this.changeFilterType(DISPLAY_UNDECIDED) }
    changeFilterToApproved() { this.changeFilterType(DISPLAY_APPROVED) }
    changeFilterToRejected() { this.changeFilterType(DISPLAY_REJECTED) }

    render() {
        return (
            <div>
                <FeedFilterControls undecidedHandler={this.changeFilterToUndecided}
                                    approvedHandler={this.changeFilterToApproved}
                                    rejectedHandler={this.changeFilterToRejected} />
                <Masonry {...this.props.masonryProps}>
                    {this.state.displayPosts}
                </Masonry>
            </div>
        )
    }
}