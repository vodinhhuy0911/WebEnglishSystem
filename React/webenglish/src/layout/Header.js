import { useEffect, useState } from "react";
import { Container, Nav, Navbar, NavDropdown } from "react-bootstrap";
import { useSelector } from "react-redux";
import { Link } from "react-router-dom";
import Apis, { endpoints } from "../configs/Apis";

export default function Headers(){
    const [category,setCategory] = useState([])
    const user = useSelector(state => state.user.user)
    
    useEffect(()=>{
        const loadCategory = async()=> {
            let res = await Apis.get(endpoints['categories'])
            setCategory(res.data)
        }
        loadCategory()

    },[])
    let path = <Link className="nav-link text-danger" to="/login">Login</Link>
    if (user != null)
        path = <Link className="nav-link text-danger" to="/">user.username</Link>
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