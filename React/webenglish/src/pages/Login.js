
import { useState } from "react";
import { Form,Button } from "react-bootstrap";
import { useDispatch } from "react-redux";
import { useHistory } from "react-router-dom";
import Apis, { endpoints } from "../configs/Apis";

export default function Login(){

    const [username,setUsername] = useState()
    const [password, setPassword] = useState()
    const dispatch = useDispatch()
    const history = useHistory()


    const loginnn= async (event)=>{ 
        console.info("s")
        event.prevenDefault()
        try{
            let info = await Apis.get(endpoints['oauth2-info'])
            console.info(info)
            let res = await Apis.post(endpoints['login'],{

                "client_id": info.data.client_id,
                "client_secret": info.data.client_secret,
                "username": username,
                "password": password,
                "grant_type": "password"

            })
            console.info(res)
            localStorage.setItem("access_token",res.data.access_token)

            let user = await Apis.get(endpoints['current-user'],{
                headers:{
                    "Authorization": `Bearer ${localStorage.getItem("access_token")}` 
                }

            })

            console.info(user)

            localStorage.setItem("user",user.data)

            dispatch({
                "type": "USER_LOGIN",
                "payload": user.data
            })
        history.push("/")
        }catch(err)
        {
            console.error("err")
        }

    }
    return(
        <div>
        <h1 className="text-center text-danger">Login</h1>
        <Form  onSubmit={loginnn}>
            <Form.Group className="mb-3" controlId="formBasicEmail">
                <Form.Label>Username</Form.Label>
                <Form.Control type="text" placeholder="Username"  
                            value={username}
                            onChange={(event) => setUsername(event.target.value)}/>
                
            </Form.Group>

            <Form.Group className="mb-3" controlId="formBasicPassword">
                <Form.Label>Password</Form.Label>
                <Form.Control type="password" placeholder="Password"  value={password} onChange={(event) => setPassword(event.target.value)}/>
            </Form.Group>
            
            <Button variant="primary" type="submit">
                Login
            </Button>
        </Form>
</div>
    )
}