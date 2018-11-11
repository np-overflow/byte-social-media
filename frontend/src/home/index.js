import React from "react"

import styles from "./index.css"
import HashtagTitle from "./HashtagTitle"
import Feed from "../common/Feed"

import { API_SOCKET_ENDPOINT_POSTS } from "../settings"

const HomeLayout = () => (
    <div>
        <HashtagTitle className={styles.banner} />
        <Feed endpoint={API_SOCKET_ENDPOINT_POSTS} />
    </div>
)

export default HomeLayout