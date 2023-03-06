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
            <ul>
            <DropDownElement text={"My Profile"} />
            <DropDownElement text={"Edit Profile"} />
            <DropDownElement text={"Log Out"} />
            </ul>            
        </div>
    </nav>);
}

function DropDownElement(props){
    return(
        <li className="dropDownElement">
            <a>[props.text]</a>
        </li>
    );
}

export default Navbar;
