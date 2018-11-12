import React from "react"

import styles from "./index.css"
import HashtagTitle from "./HashtagTitle"
import HomeFeed from "./HomeFeed"

import { API_SOCKET_ENDPOINT_POSTS } from "../settings"

const HomeLayout = () => (
    <div>
        <HashtagTitle className={styles.banner} />
        <HomeFeed endpoint={API_SOCKET_ENDPOINT_POSTS} />
    </div>
)

export default HomeLayout