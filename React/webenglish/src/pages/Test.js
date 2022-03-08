import { useEffect, useState } from "react";
import { Container, Form } from "react-bootstrap";
import { Link } from "react-router-dom";
import Apis, { endpoints } from '../configs/Apis';

export default function () {
  const [courses,setCourses] = useState([])

  useEffect(()=>{
    let loadQuestion = async () => {

      let res = await Apis.get(endpoints['multiplechoice'])
      setCourses(res.data)
      console.log(res.data)
    }
    loadQuestion()

  },[])
    return(
      <Form>
      {courses.map((m, index) => (
        <p key={index}>
          {m.content}
          <br></br>
          {
            m.answers.map((p, index) => (
              <Form.Check inline label={p.answer} name={m.id} type='radio' id={`inline-${'radio'}-1`} key={index} />
            ))
          } 
        </p>
      )
      )}
      <input type="submit" value="Submit"/>
    </Form>
    )
}