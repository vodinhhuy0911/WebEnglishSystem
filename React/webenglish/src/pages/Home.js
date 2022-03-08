import { Card, Col, Row } from "react-bootstrap";
import { Link } from "react-router-dom";

export default function Home(){
    let path = "/test"
    let multipleChoice = "/MultipleChoice"
    return(
        <Row>
          <Col md={3} xs={12}>
            <Card >
              
              <Link to={path}> 
          <Card.Img variant="top" src="https://img.freepik.com/free-vector/happy-women-learning-language-online-isolated-flat-vector-illustration-cartoon-female-characters-taking-individual-lessons-through-messenger-education-digital-technology-concept_74855-10088.jpg?w=1060" />
          </Link>
          <Card.Body>
            <Card.Title>Test</Card.Title>
            <Card.Text>
              Some quick example text to build on the card title and make up the bulk of
              the card's content.
            </Card.Text>
          </Card.Body>
        </Card>
      
          </Col>
          <Col md={3} xs={12}>
            <Card >
            <Link to={multipleChoice}> 
          <Card.Img variant="top" src="https://img.freepik.com/free-vector/happy-women-learning-language-online-isolated-flat-vector-illustration-cartoon-female-characters-taking-individual-lessons-through-messenger-education-digital-technology-concept_74855-10088.jpg?w=1060" />
          </Link>
          <Card.Body>
            <Card.Title>Multiple Choice</Card.Title>
            <Card.Text>
              Some quick example text to build on the card title and make up the bulk of
              the card's content.
            </Card.Text>
            
          </Card.Body>
        </Card>
      
          </Col>
          <Col md={3} xs={12}>
            <Card >
          <Card.Img variant="top" src="https://img.freepik.com/free-vector/happy-women-learning-language-online-isolated-flat-vector-illustration-cartoon-female-characters-taking-individual-lessons-through-messenger-education-digital-technology-concept_74855-10088.jpg?w=1060" />
          <Card.Body>
            <Card.Title>Incomplete</Card.Title>
            <Card.Text>
              Some quick example text to build on the card title and make up the bulk of
              the card's content.
            </Card.Text>
            
          </Card.Body>
        </Card>
      
          </Col>
          <Col md={3} xs={12}>
            <Card >
          <Card.Img variant="top" src="https://img.freepik.com/free-vector/happy-women-learning-language-online-isolated-flat-vector-illustration-cartoon-female-characters-taking-individual-lessons-through-messenger-education-digital-technology-concept_74855-10088.jpg?w=1060" />
          <Card.Body>
            <Card.Title>Reading Comprehension</Card.Title>
            <Card.Text>
              Some quick example text to build on the card title and make up the bulk of
              the card's content.
            </Card.Text>
            
          </Card.Body>
        </Card>
      
          </Col>
        </Row>
    )
}