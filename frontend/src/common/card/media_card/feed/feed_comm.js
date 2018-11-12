import invariant from "invariant"


// Ensure that this is consistent with the backend
export const APPROVAL_STATUS_APPROVED = "approved"
export const APPROVAL_STATUS_REJECTED = "rejected"


export function jsonSend(websocket, data) {
    websocket.send(JSON.stringify(data))
}


function _requestPosts(websocket) {
    // Naively send request immediately
    jsonSend(websocket, {"type": "all_posts"})
}


export function requestPosts(websocket) {
    // Ensure that the websocket is either opening or open
    invariant(websocket.readyState <= 1, "Websocket should either be opening or open")

    // Check if the websocket is already open
    if (websocket.readyState === 1) {
        // Send the request directly
        _requestPosts(websocket)
    } else {
        // Add an event listener for when the socket is open
        websocket.addEventListener("open", event => {
            _requestPosts(websocket)
        })
    }
}


export function sendApproval(websocket, status, postId) {
    // Websocket should be open already
    invariant(websocket.readyState === 1, "Websocket should be already open")
    // Status is either APPROVAL_STATUS_APPROVED or APPROVAL_STATUS_REJECTED
    invariant(
        [APPROVAL_STATUS_APPROVED, APPROVAL_STATUS_REJECTED].includes(status),
        `Approval status should be either ${APPROVAL_STATUS_APPROVED} or ${APPROVAL_STATUS_REJECTED}`
    )

    const payload = {
        "type": "approval",
        "post_id": postId,
        "status": status,
    }
    jsonSend(websocket, payload)
}
