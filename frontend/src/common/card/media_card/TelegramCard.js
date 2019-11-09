import React from "react"
import invariant from "invariant"

import { TELEGRAM_SRC, TELEGRAM_BG_COLOR } from "../../../settings"
import ResponsiveCard from "../ResponsiveCard"

const TelegramCard = props => {
    invariant(props.author, "TelegramCard should have an author")

    return (
        <ResponsiveCard iconSrc={TELEGRAM_SRC} titleBgColor={TELEGRAM_BG_COLOR}
              titleBright title={props.author}>
            {props.children}
        </ResponsiveCard>
    )
}

export default TelegramCard