import axios from "axios"

export let endpoints = {
    "categories": "/categories/",
    "multiplechoice":"/multiplechoice/",
    "oauth2-info": "/oauth2-info/",
    "login":"o/token/",
    "current-user":"/user/current-user/",
    "register":"/user/"
}

export default axios.create({
    baseURL: "http://127.0.0.1:8000/"

})
