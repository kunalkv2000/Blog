import React, { useState } from "react";
import AdminSidebar from "../components/admin/AdminSidebar";
import AdminPostsPanel from "../components/admin/AdminPostsPanel";
import AdminUsersPanel from "../components/admin/AdminUsersPanel";

function AdminDashboard({ currentUser, onLogout }) {
    const [tab, setTab] = useState("posts"); // 'posts' | 'users'

    return (
        <div className="min-h-screen flex bg-slate-100 text-slate-900">
            <AdminSidebar
                currentUser={currentUser}
                activeTab={tab}
                onTabChange={setTab}
                onLogout={onLogout}
            />

            {/* Main content */}
            <main className="flex-1 p-6">
                {tab === "posts" ? <AdminPostsPanel /> : <AdminUsersPanel />}
            </main>
        </div>
    );
}

export default AdminDashboard;
