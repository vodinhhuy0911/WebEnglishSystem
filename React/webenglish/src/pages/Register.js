import { useRef, useState } from "react"

import { Form,Button } from "react-bootstrap";
import { useHistory } from "react-router-dom";
import Apis, { endpoints } from "../configs/Apis";

export default function Register()
{
    const [username,setUsername] = useState()
    const [password, setPassword] = useState()
    const [confirmPassword, setConfirmPassword] = useState()
    const [firstName,setFirstName] = useState()
    const [lastName, setLastName] = useState()
    const [email, setEmail] = useState()
    const history = useHistory()

    const register = (event) =>{
        event.preventDefault()

        let registerUser = async() =>{
            const formData = new FormData()
            formData.append("first_name",firstName)
            formData.append("last_name",lastName)
            formData.append("email",email)
            formData.append("password",password)
            formData.append("username",username)

            let res = await Apis.post(endpoints['register'],formData,{
                headers: {
                    "Content-Type": "multipart/form-data"
                }

            })

            console.info(res.data)
            history.push("/login")
        }

        if(password !== null && password === confirmPassword){
            registerUser()
        }
    }



    return (
    <>
    <h1 className="text-center text-success">Register</h1>
    <Form  onSubmit={register}>
            <RegisterForm id="firstName" label = "First Name" type = "text" value ={firstName} change = {(event)=> setFirstName(event.target.value)}/>
            <RegisterForm id="lastName" label = "Last Name" type = "text" value ={lastName} change = {(event)=> setLastName(event.target.value)}/>  
            <RegisterForm id="email" label = "Email" type = "email" value ={email} change = {(event)=> setEmail(event.target.value)}/>  
            <RegisterForm id="userName" label = "User name" type = "text" value ={username} change = {(event)=> setUsername(event.target.value)}/>  
            <RegisterForm id="password" label = "Password" type = "password" value ={password} change = {(event)=> setPassword(event.target.value)}/>  
            <RegisterForm id="confirmPassword" label = "Confirm Password" type = "password" value ={confirmPassword} change = {(event)=> setConfirmPassword(event.target.value)}/>  
            {/* <RegisterForm id="avatar" label = "Avatar" type = "file" ref={avatar}/>  */}

            <Button variant="primary" type="submit">
                Register
            </Button>
        </Form>
        </>
    )
}

function RegisterForm(props){
    return (
        <Form.Group className="mb-3" controlId={props.id}>
                <Form.Label>{props.label}</Form.Label>
                <Form.Control type={props.type}   value={props.value} onChange={props.change}/>
            </Form.Group>
    )
}