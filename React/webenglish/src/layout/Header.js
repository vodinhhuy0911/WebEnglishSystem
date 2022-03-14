import { useEffect, useState } from "react";
import { Container, Nav, Navbar, NavDropdown } from "react-bootstrap";
import cookies from "react-cookies";
import { useDispatch, useSelector } from "react-redux";
import { Link } from "react-router-dom";
import { logoutUser } from "../ActionCreater/UserCreate";
import Apis, { endpoints } from "../configs/Apis";

export default function Headers(){
    const [category,setCategory] = useState([])
    const user = useSelector(state => state.user.user)
    const dispatch = useDispatch()
    
    useEffect(()=>{
        const loadCategory = async()=> {
            let res = await Apis.get(endpoints['categories'])
            setCategory(res.data)
        }
        loadCategory()

    },[])

    const logout = (event) =>{
        event.preventDefault()
        cookies.remove("access_token")
        cookies.remove("user")
        dispatch(logoutUser)

    }


    let path = 
    <>
    <Link className="nav-link text-danger" to="/login">Login</Link>
    <Link className="nav-link text-danger" to="/register">Register</Link>
    </>

    if (user !== null && user !== undefined)
    {
        path = 
        <>
        <Link className="nav-link text-danger" to="/">{user.username}</Link>
        <Link className="nav-link text-danger" onClick={logout}>Logout</Link>
        </>
    }
    return (
        <Navbar bg="light" expand="lg">
            <Container>
                <Navbar.Brand href="#home">React-Bootstrap</Navbar.Brand>
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav">
               
                <NavDropdown title="Cateogry" id="basic-nav-dropdown">
                {category.map(c =><NavDropdown.Item href="#action/3.1">{c.name}</NavDropdown.Item>)}
                
                
        </NavDropdown>
        {path}
                </Navbar.Collapse>
            </Container>
        </Navbar>
    )
}