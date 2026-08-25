import { Outlet } from "react-router-dom";
import ThemeToggle from "../components/ThemeToggle.jsx";
import './layout.css'

function MainLayout () {
    return (
        <>
            <header>
                <h2>
                    TaskWyrm
                </h2>
                <ThemeToggle />
            </header>

            <main>
                <Outlet />
            </main>

            <footer>
                TaskWyrm 2026
            </footer>
        </>
    )
}

export default MainLayout;