import React from "react"

import Feed from "../common/Feed"
import { API_SOCKET_ENDPOINT_ADMIN_POSTS } from "../settings"

const AdminLayout = () => (
    <div>
        <Feed endpoint={API_SOCKET_ENDPOINT_ADMIN_POSTS} />
    </div>
)

export default AdminLayout