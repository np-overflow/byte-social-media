import React from "react"

import Masonry from "react-masonry-component"
import TwitterCard from "./TwitterCard"
import FacebookCard from "./FacebookCard"
import InstagramCard from "./InstagramCard"

import MediaImage from "./MediaImage"
import CardCaption from "./CardCaption"

export default class Feed extends React.Component {
    constructor(props) {
        super(props)

        this.state = {
            ws: null,
            posts: []
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
            const post = this.toPostHtml(JSON.parse(event.data))
            this.setState(prevState => ({
                posts: prevState.posts.concat(post)
            }))
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

    render() {
        return (
            <Masonry {...this.props.masonryProps}>
                {this.state.posts}
            </Masonry>
        );
    }
}