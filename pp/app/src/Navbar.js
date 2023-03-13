import './App.css';

import React, {useState, useEffect, useRef} from 'react';

function Navbar(){
    const [open, setOpen] = useState(false);
    return (<nav className="nav">
        <a href="/" className="site-title">Ticket Master</a>
        <ul>
            <li>
                <a href="/login">Login</a>
            </li>
            <li>
                <div className='toggle' onClick={()=>{setOpen(!open)}}><p>Profile</p></div>
            </li>
        </ul>
        <div className={`DropDown ${open? 'active' : 'inactive'}`}>
            <ul id='bob'>
                <DropDownElement name="My Profile" link=""/>
                <DropDownElement name="Edit Profile" link=""/>
                <DropDownElement name="Log Out" link=""/>
            </ul>            
        </div>
    </nav>);
}

function DropDownElement(props){
    return(
        <li className="dropDownElement">
            <a href={props.link}>{props.name}</a>
        </li>
    );
}

export default Navbar;
