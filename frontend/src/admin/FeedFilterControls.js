import React from "react"

export default class FeedFilterControls extends React.Component {
    constructor(props) {
        super(props)

        this.state = {
            all: true,
            approved: false,
            rejected: false,
        }
        this.handleAllClick = this.handleAllClick.bind(this)
        this.handleApprovedClick = this.handleApprovedClick.bind(this)
        this.handleRejectedClick = this.handleRejectedClick.bind(this)
    }

    handleAllClick(event) {
        this.setState({
            all: true,
            approved: false,
            rejected: false,
        })
        this.props.allHandler()
    }

    handleApprovedClick(event) {
        this.setState({
            all: false,
            approved: true,
            rejected: false,
        })
        this.props.approvedHandler()
    }

    handleRejectedClick(event) {
        this.setState({
            all: false,
            approved: false,
            rejected: true,
        })
        this.props.rejectedHandler()
    }

    render() {
        return (
            <ul className="nav nav-pills">
                <li className="nav-item">
                    <a onClick={this.handleAllClick}
                       href="#"
                       className={`nav-link ${this.state.all? "active": ""}`}>All</a>
                </li>
                <li className="nav-item">
                    <a onClick={this.handleApprovedClick}
                       href="#"
                       className={`nav-link ${this.state.approved? "active": ""}`}>Approved</a>
                </li>
                <li className="nav-item">
                    <a onClick={this.handleRejectedClick}
                       href="#"
                       className={`nav-link ${this.state.rejected? "active": ""}`}>Rejected</a>
                </li>
            </ul>
        )
    }
}
