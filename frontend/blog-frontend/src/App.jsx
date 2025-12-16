import React, { useState, useEffect } from "react";
import "./index.css";

import LoginPage from "./pages/LoginPage";
import AdminDashboard from "./pages/AdminDashboard";
import UserBlogPage from "./pages/UserBlogPage";
import { apiGet, apiPost } from "./utils/api";


export default function App() {
  const [currentUser, setCurrentUser] = useState(null);

  function handleLogin(user) {
    setCurrentUser(user);
  }

  function handleLogout() {
    apiPost("/auth/logout", {}).finally(() => setCurrentUser(null));
  }

  useEffect(() => {
    let mounted = true;
    (async function restore() {
      try {
        const res = await apiGet("/auth/me");
        if (!mounted) return;
        if (res.ok) {
          const user = await res.json();
          setCurrentUser(user);
        } else {
          setCurrentUser(null);
        }
      } catch (err) {
        setCurrentUser(null);
      }
    })();
    return () => {
      mounted = false;
    };
  }, []);

  if (!currentUser) {
    return <LoginPage onLogin={handleLogin} />;
  }

  if (currentUser.role === "admin") {
    return <AdminDashboard currentUser={currentUser} onLogout={handleLogout} />;
  }

  return <UserBlogPage currentUser={currentUser} onLogout={handleLogout} />;
}
