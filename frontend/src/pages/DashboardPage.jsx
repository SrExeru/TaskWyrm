import { useEffect, useState } from "react";
import { api } from "../services";



function DashboardPage () {
    const [userData, setUserData] = useState(null)

    useEffect(() => {
        api.get('/user/me')
            .then((response) => {
                setUserData(response.data);
            })
            .catch((error) => {
                console.error('Loading user error:', error)
            })
    }, []);
    
    return (
        <h1>
            Welcome {userData?.username}
        </h1>
    )
}

export default DashboardPage;