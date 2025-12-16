// src/components/user/UserHeader.jsx
import React from "react";
import Button from "../ui/Button";

function UserHeader({ currentUser, onLogout }) {
    return (
        <header className="bg-white border-b px-6 py-3 flex justify-between items-center">
            <div>
                <h1 className="text-lg font-semibold text-slate-800">Blog Portal</h1>
                <p className="text-xs text-slate-500">
                    Logged in as{" "}
                    <span className="font-semibold">
                        {currentUser.name} ({currentUser.email})
                    </span>
                </p>
            </div>
            <Button
                variant="delete"
                size="sm"
                onClick={onLogout}
            >
                Logout
            </Button>
        </header>
    );
}

export default UserHeader;
