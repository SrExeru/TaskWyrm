import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../services";
import '../styles/LoginPage.css'

function LoginErrorMessage ({ message }) {
    if (message) {
        return <p id="login_error">{ message }</p>
    }
    return <p id="login_error"></p>
}

function LoginPage () {
    const navigate = useNavigate()

    const [loginError, setLoginError] = useState(null);
    const [validLogin, setValidLogin] = useState(false);

    const handleLogin = async (e) => {
        e.preventDefault();

        const form = e.target;
        const form_data = new FormData(form);

        await api.post('/auth/login', Object.fromEntries(form_data))
            .then((response) => {
                localStorage.setItem('access_token', response.data.access_token);

                setValidLogin(true);
            })
            .catch((error) => {
                setLoginError(error.response?.data?.detail || 'Login error.');
            })
            .finally(() => {
                if (validLogin) {
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
                Login
            </h1>
            <input type="hidden" name="decive" value={ getDeviceName() }/>
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

            <LoginErrorMessage message={ loginError } />

            <input type="submit" value="Login" />
        </form>
    )
}

export default LoginPage;