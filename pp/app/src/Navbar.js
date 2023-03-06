import './App.css';

import React, {useState, useEffect, useRef} from 'react';

function Navbar(){
    const [open, setOpen] = useState(false);
    return <nav className="nav">
        <a href="/" className="site-title">Ticket Master</a>
        <ul>
            <li>
                <a href="/login">Login</a>
            </li>
            <li>
                <div className='toggle' onClick={()=>{setOpen(!open)}}>Profile</div>
                <div className={`DropDown ${open? 'active' : 'inactive'}`}>
                <ul>
                    <DropDownElement text = {"My Profile"}/>
                </ul>
                    
                </div>
            </li>
            
        </ul>
    </nav>

}

function DropDownElement(props){
    return
        <li className="dropDownItem">
            <a>[props.text]</a>
        </li>
    
}

export default Navbar;
