import React from "react"

import Masonry from "react-masonry-component"
import TwitterCard from  "../TwitterCard"
import FacebookCard from "../FacebookCard"
import InstagramCard from "../InstagramCard"

import MediaImage from "../../../MediaImage"
import CardCaption from "../../CardCaption"

const DISPLAY_APPROVED = "approved"
const DISPLAY_ALL = "all"
const DISPLAY_REJECTED = "rejected"

export default class Feed extends React.Component {
    constructor(props) {
        super(props)

        this.state = {
            ws: null,
            posts: [],
            displayPosts: [],
            displayType: "all",
        }
    }

    toMediaHtml(mediaJson) {
        if (!mediaJson) {
            return
        }

        switch (mediaJson["type"]) {
            case "image":
                return <MediaImage src={mediaJson["src"]} />
                break
        }
    }

    toPostHtml(mediaJson) {
        let media = this.toMediaHtml(mediaJson["media"])
        switch (mediaJson["platform"]) {
            case "twitter":
                return (
                    <TwitterCard key={mediaJson["id"]} author={mediaJson["author"]}>
                        {media}
                        <CardCaption>{mediaJson["caption"]}</CardCaption>
                    </TwitterCard>
                )
            case "instagram":
                return (
                    <InstagramCard key={mediaJson["id"]} author={mediaJson["author"]}>
                        {media}
                        <CardCaption>{mediaJson["caption"]}</CardCaption>
                    </InstagramCard>
                )
            case "facebook":
                return (
                    <FacebookCard key={mediaJson["id"]} author={mediaJson["author"]}>
                        {media}
                        <CardCaption>{mediaJson["caption"]}</CardCaption>
                    </FacebookCard>
                )
        }
    }

    createWebSocket() {
        const ws = new WebSocket(this.props.endpoint)
        ws.addEventListener("message", event => {
            // Create post HTML
            const post_json = JSON.parse(event.data)
            const post = this.toPostHtml(post_json)

            // Update state
            this.setState(prevState => {
                let newState = {
                    posts: prevState.posts.concat(post_json)
                }

                // Update displayPosts based on post type
                switch (prevState.displayType) {
                    case DISPLAY_ALL:
                        newState.displayPosts = prevState.displayPosts.concat(post)
                        break
                    case DISPLAY_APPROVED:
                        if (post_json["isApproved"]) {
                            newState.displayPosts = prevState.displayPosts.concat(post)
                        }
                        break
                    case DISPLAY_REJECTED:
                        if (post_json["rejected"]) {
                            newState.displayPosts = prevState.displayPosts.concat(post)
                        }
                        break
                }
                return newState
            })
        })

        ws.addEventListener("open", event => {
            ws.send(JSON.stringify({"type": "all_posts"}))
        })

        return ws
    }

    componentDidMount() {
        this.setState({
            ws: this.createWebSocket()
        })
    }

    changePostDisplay(oldType, newType) {
        if (oldType === newType) {
            return
        }

        // Filter out the posts to display
        // Create filter functions for different types
        let filterFn
        switch (newType) {
            case DISPLAY_ALL:
                filterFn = post => true
                break
            case DISPLAY_APPROVED:
                filterFn = post => post.isApproved
                break
            case DISPLAY_REJECTED:
                filterFn = post => !post.isApproved
                break
        }

        this.setState({
            displayPosts: this.state.posts.filter(filterFn).map(this.toPostHtml.bind(this)),
            displayType: newType,
        })
    }

    handleClickAllPosts() {
        this.changePostDisplay(this.state.displayType, DISPLAY_ALL)
    }
    
    handleClickApprovedPosts() {
        this.changePostDisplay(this.state.displayType, DISPLAY_APPROVED)
    }

    handleClickRejectedPosts() {
        this.changePostDisplay(this.state.displayType, DISPLAY_REJECTED)
    }

    render() {
        let controls
        if (this.props.controls) {
            controls = (
                <div>
                    <button onClick={this.handleClickAllPosts.bind(this)}>All</button>
                    <button onClick={this.handleClickApprovedPosts.bind(this)}>Approved</button>
                    <button onClick={this.handleClickRejectedPosts.bind(this)}>Rejected</button>
                </div>
            )
        }
        return (
            <div>
                {controls}
                <Masonry {...this.props.masonryProps}>
                    {this.state.displayPosts}
                </Masonry>
            </div>
        )
    }
}