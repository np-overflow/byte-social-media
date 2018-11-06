import React from "react"
import ReactDOM from "react-dom"

import HomeLayout from "./home"

const MainLayout = () => (
    <HomeLayout />
)

const app = document.getElementById("app")
ReactDOM.render(<MainLayout />, app)