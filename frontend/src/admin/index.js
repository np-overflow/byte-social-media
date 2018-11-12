import React from "react"

import AdminFeed from "./AdminFeed"
import { API_SOCKET_ENDPOINT_ADMIN_POSTS } from "../settings"

const AdminLayout = () => (
    <div>
        <AdminFeed endpoint={API_SOCKET_ENDPOINT_ADMIN_POSTS} controls />
    </div>
)

export default AdminLayout