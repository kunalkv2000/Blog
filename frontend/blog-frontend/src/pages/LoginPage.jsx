import React from "react";
import "../index.css";
import LoginForm from "../components/auth/LoginForm";

function LoginPage({ onLogin }) {
    return (
        <div className="min-h-screen flex items-center justify-center bg-slate-100">
            <LoginForm onLogin={onLogin} />
        </div>
    );
}

export default LoginPage;
