import { combineReducers } from "redux";
import userReducers from "./UserReducers";

const mainReducers = combineReducers({
    'user': userReducers,
})

export default mainReducers