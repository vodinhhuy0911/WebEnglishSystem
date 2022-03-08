import { useEffect, useState } from "react";
import { Container, Nav, Navbar, NavDropdown } from "react-bootstrap";
import { Link } from "react-router-dom";
import Apis, { endpoints } from "../configs/Apis";

export default function Headers(){
    const [category,setCategory] = useState([])
    
    useEffect(()=>{
        const loadCategory = async()=> {
            let res = await Apis.get(endpoints['categories'])
            setCategory(res.data)
        }
        loadCategory()

    },[])

    return (
        <Navbar bg="light" expand="lg">
            <Container>
                <Navbar.Brand href="#home">React-Bootstrap</Navbar.Brand>
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav">
               
                <NavDropdown title="Cateogry" id="basic-nav-dropdown">
                {category.map(c =><NavDropdown.Item href="#action/3.1">{c.name}</NavDropdown.Item>)}
          
          
        </NavDropdown>
                </Navbar.Collapse>
            </Container>
        </Navbar>
    )
}