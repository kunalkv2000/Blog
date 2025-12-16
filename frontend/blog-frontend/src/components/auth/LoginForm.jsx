// src/components/auth/LoginForm.jsx
import React, { useState } from "react";

function LoginForm({ onLogin }) {
    const API_BASE = import.meta.env.VITE_API_BASE;
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [status, setStatus] = useState("");

    async function handleSubmit(e) {
        e.preventDefault();
        console.log("Form submitted!", { email, password });
        setStatus("");
        try {
            const res = await fetch(`${API_BASE}/auth/login`, {
                method: "POST",
                credentials: "include",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password }),
            });
            console.log("Response received:", res.status);
            if (!res.ok) {
                const data = await res.json().catch(() => ({}));
                throw new Error(data.detail || "Invalid credentials");
            }
            const user = await res.json();
            console.log("Login successful:", user);
            onLogin(user); // {id, name, email, role}
        } catch (err) {
            console.error("Login error:", err);
            setStatus(err.message || "Login failed");
        }
    }

    return (
        <div className="bg-white shadow-xl rounded-xl px-8 py-6 w-full max-w-md">
            <h1 className="text-2xl font-bold mb-2 text-slate-800 text-center">
                Blog Login
            </h1>
            <p className="text-xs text-slate-500 mb-4 text-center">
                Credentials are validated from PostgreSQL.
            </p>

            {status && (
                <div className="mb-3 text-xs text-red-700 bg-red-50 border border-red-200 px-3 py-2 rounded-lg">
                    {status}
                </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4 text-sm">
                <div>
                    <label className="block text-xs font-medium text-slate-600 mb-1">
                        Email
                    </label>
                    <input
                        type="email"
                        className="w-full border rounded-lg px-3 py-2 border-slate-300 focus:outline-none focus:ring-2 focus:ring-sky-500"
                        placeholder="you@example.com"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                </div>

                <div>
                    <label className="block text-xs font-medium text-slate-600 mb-1">
                        Password
                    </label>
                    <input
                        type="password"
                        className="w-full border rounded-lg px-3 py-2 border-slate-300 focus:outline-none focus:ring-2 focus:ring-sky-500"
                        placeholder="••••••••"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>

                <button
                    type="submit"
                    className="w-full bg-sky-600 hover:bg-sky-700 text-white font-medium py-2 rounded-lg transition"
                >
                    Login
                </button>
            </form>
        </div>
    );
}

export default LoginForm;
