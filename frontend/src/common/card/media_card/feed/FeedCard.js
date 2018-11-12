import React from "react"
import invariant from "invariant"

import FeedMedia from "./FeedMedia"
import CardCaption from "../../CardCaption"
import TwitterCard from "../FacebookCard";
import FacebookCard from "../FacebookCard";
import InstagramCard from "../InstagramCard";

const FeedCard = props => {
    invariant(props.cardJson, "FeedCard should have a cardJson prop")

    const data = props.cardJson

    let media;
    if (data["media"]) {
        media = <FeedMedia mediaJson={data["media"]} />
    }
    const caption = <CardCaption>{data["caption"]}</CardCaption>

    const cardProps = {
        author: data["author"],
    }

    switch (data["platform"]) {
        case "twitter":
            return <TwitterCard {...cardProps}>{media}{caption}{props.children}</TwitterCard>
        case "instagram":
            return <InstagramCard {...cardProps}>{media}{caption}{props.children}</InstagramCard>
        case "facebook":
            return <FacebookCard {...cardProps}>{media}{caption}{props.children}</FacebookCard>
    }
}

export default FeedCard