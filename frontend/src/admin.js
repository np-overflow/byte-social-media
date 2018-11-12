import React from "react"
import ReactDOM from "react-dom"

import AdminLayout from "./admin/index"

const MainLayout = () => (
    <AdminLayout />
)

const app = document.getElementById("app")
ReactDOM.render(<MainLayout />, app)