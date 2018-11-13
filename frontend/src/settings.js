function construct_ws_url(endpoint) {
    let loc = window.location, new_uri;
    if (loc.protocol === "https:") {
        new_uri = "wss:"
    } else {
        new_uri = "ws:"
    }

    new_uri += "//" + loc.host + "/" + endpoint

    return new_uri
}

export const FACEBOOK_SRC = "/assets/imgs/facebook_logo/flogo-72.svg"
export const FACEBOOK_BG_COLOR = "#3351a2"

export const TWITTER_SRC = "/assets/imgs/twitter_logo/twitter-logo.svg"
export const TWITTER_BG_COLOR = "#1D8DEE"

export const INSTAGRAM_SRC = "/assets/imgs/instagram_logo/instagram-logo.svg"
export const INSTAGRAM_BG_COLOR = "#CD1662"

export const API_ENDPOINT_HASHTAGS = "/api/hashtags/"
export const API_SOCKET_ENDPOINT_POSTS = construct_ws_url("ws/posts/")
export const API_SOCKET_ENDPOINT_ADMIN_POSTS = construct_ws_url("ws/admin/")
