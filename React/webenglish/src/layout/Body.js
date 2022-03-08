
import { BrowserRouter, Switch, Route } from 'react-router-dom';

import Home from '../pages/Home';
import MultipleChoice from '../pages/MultipleChoice';
import Test from '../pages/Test';
import Footer from './Footer';
import Headers from './Header';


export default function Body(){
    return (
        
        <BrowserRouter>
            <Headers/>
            <Switch>
                <Route exact path="/"  component={Home}/>
                <Route exact path="/multiplechoice/"  component={MultipleChoice}/>
                <Route exact path ="/test/" component={Test}></Route>
            </Switch>
            <Footer/>
        </BrowserRouter>
     
    
    )
}