
import { useState } from "react";
import { Form,Button } from "react-bootstrap";
import cookies from "react-cookies";
import { useDispatch } from "react-redux";
import { useHistory } from "react-router-dom";
import { loginUser } from "../ActionCreater/UserCreate";
import Apis, { endpoints } from "../configs/Apis";

export default function Login(){

    const [username,setUsername] = useState()
    const [password, setPassword] = useState()
    const dispatch = useDispatch()
    const history = useHistory()


    const login = async (event)=>{ 
        console.info("s")
        event.preventDefault()
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
            cookies.save("access_token",res.data.access_token)

            let user = await Apis.get(endpoints['current-user'],{
                headers:{
                    "Authorization": `Bearer ${cookies.load("access_token")}` 
                }

            })

            console.info(user)

            cookies.save("user",user.data)

            dispatch(loginUser(user.data))
        history.push("/")
        }catch(err)
        {
            console.error("err")
        }

    }
    return(
        <div>
        <h1 className="text-center text-danger">Login</h1>
        <Form  onSubmit={login}>
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