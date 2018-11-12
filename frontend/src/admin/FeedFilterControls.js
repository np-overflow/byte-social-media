import React from "react"

const FeedFilterControls = props => (
    <div>
        <button className="btn btn-light" onClick={props.allHandler}>All</button>
        <button className="btn btn-success" onClick={props.approvedHandler}>Approved</button>
        <button className="btn btn-danger" onClick={props.rejectedHandler}>Rejected</button>
    </div>
)

export default FeedFilterControls