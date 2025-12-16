import React from "react";

function AdminSidebar({ currentUser, activeTab, onTabChange, onLogout }) {
    return (
        <aside className="w-64 bg-slate-900 text-slate-100 flex flex-col ">
            <div className="p-4 border-b border-slate-800">
                <h1 className="text-xl font-bold tracking-tight">Admin Panel</h1>
                <p className="text-xs text-slate-400">
                    {currentUser.email} ({currentUser.role})
                </p>
            </div>

            <nav className="flex-1 p-4 space-y-2 text-sm">
                <div className="text-xs text-slate-500 uppercase mb-1">Manage</div>
                <button
                    onClick={() => onTabChange("posts")}
                    className={`w-full text-left px-3 py-2 rounded-md transition ${activeTab === "posts"
                        ? "bg-slate-800 text-white"
                        : "hover:bg-slate-800/60"
                        }`}
                >
                    Blog Posts
                </button>
                <button
                    onClick={() => onTabChange("users")}
                    className={`w-full text-left px-3 py-2 rounded-md transition ${activeTab === "users"
                        ? "bg-slate-800 text-white"
                        : "hover:bg-slate-800/60"
                        }`}
                >
                    Users
                </button>
            </nav>

            <div className="p-4 border-t border-slate-800 text-xs flex justify-between items-center">
                <span>{currentUser.name}</span>
                <button
                    onClick={onLogout}
                    className="text-red-300 hover:text-red-200 font-semibold"
                >
                    Logout
                </button>
            </div>
        </aside>
    );
}

export default AdminSidebar;
