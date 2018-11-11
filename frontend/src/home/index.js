import React from "react"

import styles from "./index.css"
import HashtagTitle from "./HashtagTitle"
import Feed from "./Feed"

const HomeLayout = () => (
    <div>
        <HashtagTitle className={styles.banner} />
        <Feed />
    </div>
)

export default HomeLayout