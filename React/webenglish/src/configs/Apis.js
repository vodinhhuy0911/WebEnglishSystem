import axios from "axios"

export let endpoints = {
    "categories": "/categories/",
    "multiplechoice":"/multiplechoice/"
}

export default axios.create({
    baseURL: "http://127.0.0.1:8000/"

})
