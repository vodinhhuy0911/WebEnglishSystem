
import { Card, Col, Form, Row, Button, InputGroup, FormControl } from "react-bootstrap";
import { Link } from "react-router-dom";

export default function MultipleChoice(){
    let path = "/test"
    let multipleChoice = "/MultipleChoice"
    return(
        <Form>
  <InputGroup>
    <InputGroup.Text>Question</InputGroup.Text>
    <FormControl as="textarea" aria-label="With textarea" />
  </InputGroup>
  <Form.Group className="mb-3" controlId="formBasicEmail">
    <Form.Label>Answer A</Form.Label>
    <Form.Control type="email" placeholder="Answer A" />
  </Form.Group>
  <Form.Group className="mb-3" controlId="formBasicEmail">
    <Form.Label>Answer B</Form.Label>
    <Form.Control type="email" placeholder="Answer B" />
  </Form.Group>
  <Form.Group className="mb-3" controlId="formBasicEmail">
    <Form.Label>Answer C</Form.Label>
    <Form.Control type="email" placeholder="Answer C" />
  </Form.Group>
  <Form.Group className="mb-3" controlId="formBasicEmail">
    <Form.Label>Answer D</Form.Label>
    <Form.Control type="email" placeholder="Answer D" />
  </Form.Group>
  <Button variant="primary" type="submit">
    Submit
  </Button>
</Form>
    )
}