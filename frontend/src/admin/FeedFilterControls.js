import React from "react"

export default class FeedFilterControls extends React.Component {
    constructor(props) {
        super(props)

        this.state = {
            undecided: true,
            approved: false,
            rejected: false,
        }
        this.handleUndecidedClick = this.handleUndecidedClick.bind(this)
        this.handleApprovedClick = this.handleApprovedClick.bind(this)
        this.handleRejectedClick = this.handleRejectedClick.bind(this)
    }

    handleUndecidedClick(event) {
        this.setState({
            undecided: true,
            approved: false,
            rejected: false,
        })
        this.props.undecidedHandler()
    }

    handleApprovedClick(event) {
        this.setState({
            undecided: false,
            approved: true,
            rejected: false,
        })
        this.props.approvedHandler()
    }

    handleRejectedClick(event) {
        this.setState({
            undecided: false,
            approved: false,
            rejected: true,
        })
        this.props.rejectedHandler()
    }

    render() {
        return (
            <ul className="nav nav-pills">
                <li className="nav-item">
                    <a onClick={this.handleUndecidedClick}
                       href="#"
                       className={`nav-link ${this.state.undecided? "active": ""}`}>Undecided</a>
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
