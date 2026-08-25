import { UseTheme } from "../context/ThemeProvider.jsx";

function ThemeToggle () {
    const { theme, toggleTheme } = UseTheme();

    return (
        <button onClick={toggleTheme}>
            {theme === 'light' ? '🌙 Modo Oscuro' : '☀️ Modo Claro'}
        </button>
    )
}

export default ThemeToggle;