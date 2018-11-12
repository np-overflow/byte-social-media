import React from "react"
import invariant from "invariant"

import FeedCard from "../common/card/media_card/feed/FeedCard";
import CardApprovalControls from "../common/card/CardApprovalControls"
import { sendApproval, APPROVAL_STATUS_APPROVED, APPROVAL_STATUS_REJECTED } from "../common/card/media_card/feed/feed_comm"


const AdminFeedCard = props => {
    invariant(props.cardJson, "AdminFeedCard should have cardJson prop")

    function approve(event) {
        sendApproval(props.websocket, APPROVAL_STATUS_APPROVED, props.cardJson["id"])
    }

    function reject(event) {
        sendApproval(props.websocket, APPROVAL_STATUS_REJECTED, props.cardJson["id"])
    }

    return (
        <FeedCard cardJson={props.cardJson}>
            <CardApprovalControls approveHandler={approve} rejectHandler={reject} />
        </FeedCard>
    )
}

export default AdminFeedCard