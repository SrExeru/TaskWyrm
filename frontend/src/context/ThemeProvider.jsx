import { createContext, useContext, useEffect, useState } from 'react';

const ThemeContext = createContext();
const UseTheme = () => useContext(ThemeContext);

function ThemeProvider ({ children }) {
    const [theme, setTheme] = useState(() => {
        const savedTheme = localStorage.getItem('theme');

        if (savedTheme) return savedTheme;
        return window.matchMedia('(prefers-color-theme: dark)').matches ? 'dark' : 'light'
    });

    useEffect(() => {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme)
    }, [theme]);

    const toggleTheme = () => {
        setTheme((prev) => (prev === 'light' ? 'dark' : 'light'));
    };

    return (
        <ThemeContext.Provider value={{ theme, toggleTheme }}>
            { children }
        </ThemeContext.Provider>
    );
}

export { UseTheme, ThemeProvider };