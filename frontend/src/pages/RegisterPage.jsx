import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../services";
import '../styles/RegisterPage.css'

function RegisterErrorMessage ({ message }) {
    if (message) {
        return <p id="regiser_error">{ message }</p>
    }
    return <p id="regiser_error"></p>
}

function RegisterPage () {
    const navigate = useNavigate()

    const [registerError, setRegisterError] = useState(null);
    const [validRegister, setValidRegister] = useState(false);

    const handleLogin = async (e) => {
        e.preventDefault();

        const form = e.target;
        const form_data = new FormData(form);

        await api.post('/auth/register', Object.fromEntries(form_data))
            .then((response) => {
                localStorage.setItem('access_token', response.data.token);

                setValidRegister(true);
            })
            .catch((error) => {
                setRegisterError(error.response?.data?.detail || 'Register error.');
            })
            .finally(() => {
                if (validRegister) {
                    navigate('/dashboard')
                }
            });
    }

    const getDeviceName = () => {
        const ua = navigator.userAgent;
  
        if (/mobile/i.test(ua)) return 'Mobile Device';
        if (/iPad|iPhone|iPod/.test(ua)) return 'iOS Device';
        if (/Android/.test(ua)) return 'Android Device';
        if (/Macintosh/.test(ua)) return 'Mac';
        if (/Windows/.test(ua)) return 'Windows PC';
        if (/Linux/.test(ua)) return 'Linux PC';
  
        return 'Browser Client';
    };


    const device = getDeviceName();

    return (
        <form onSubmit={ handleLogin }>
            <h1>
                Register
            </h1>
            <input type="hidden" name="device" value={ device }/>
            <div className="form_question">
                <label htmlFor="username">
                    Username
                </label>
                <input type="text" name="username" id="username" required={ true }/>
            </div>
            <div className="form_question">
                <label htmlFor="email">
                    Email
                </label>
                <input type="email" name="email" id="email" required={ true }/>
            </div>
            <div className="form_question">
                <label htmlFor="password">
                    Password
                </label>
                <input type="password" name="password" id="password" required={ true }/>
            </div>

            <RegisterErrorMessage message={ registerError } />

            <input type="submit" value="Register" />
        </form>
    )
}

export default RegisterPage;