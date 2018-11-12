import React from "react"
import invariant from "invariant"

import MediaImage from "../../../MediaImage";

const FeedMedia = props => {
    invariant(props.mediaJson, "FeedMedia should have mediaJson prop")

    const data = props.mediaJson

    switch (data["type"]) {
        case "image":
            return <MediaImage src={data["src"]} />
            break
    }
}

export default FeedMedia