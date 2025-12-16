// src/components/admin/users/CreateUserModal.jsx
import React, { useState } from "react";
import ModalForm from "../../ui/ModalForm";
import { apiPost } from "../../../utils/api";

function CreateUserModal({ isOpen, onClose, onSuccess }) {
    const [email, setEmail] = useState("");
    const [name, setName] = useState("");
    const [role, setRole] = useState("user");
    const [password, setPassword] = useState("");
    const [status, setStatus] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();
        setStatus("");
        try {
            const res = await apiPost(`/users/`, { email, name, role, password });
            if (!res.ok) {
                const data = await res.json().catch(() => ({}));
                throw new Error(data.detail || "Error creating user");
            }
            setStatus("✅ User created");
            setEmail("");
            setName("");
            setRole("user");
            setPassword("");
            onSuccess();
            onClose();
        } catch (err) {
            setStatus(err.message || "Error creating user");
        }
    };

    if (!isOpen) return null;

    return (
        <ModalForm
            title="Create User"
            onCancel={onClose}
            onSubmit={handleSubmit}
            status={status}
            submitLabel="Create"
        >
            <div>
                <label className="block text-xs font-medium text-slate-600 mb-1">
                    Email
                </label>
                <input
                    className="w-full border border-slate-300 rounded-lg px-2 py-1.5 focus:ring-2 focus:ring-sky-500 text-sm"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />
            </div>
            <div>
                <label className="block text-xs font-medium text-slate-600 mb-1">
                    Name
                </label>
                <input
                    className="w-full border border-slate-300 rounded-lg px-2 py-1.5 focus:ring-2 focus:ring-sky-500 text-sm"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                />
            </div>
            <div>
                <label className="block text-xs font-medium text-slate-600 mb-1">
                    Role
                </label>
                <select
                    className="w-full border border-slate-300 rounded-lg px-2 py-1.5 focus:ring-2 focus:ring-sky-500 text-sm"
                    value={role}
                    onChange={(e) => setRole(e.target.value)}
                >
                    <option value="user">user</option>
                    <option value="admin">admin</option>
                </select>
            </div>
            <div>
                <label className="block text-xs font-medium text-slate-600 mb-1">
                    Password
                </label>
                <input
                    type="password"
                    className="w-full border border-slate-300 rounded-lg px-2 py-1.5 focus:ring-2 focus:ring-sky-500 text-sm"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
            </div>
        </ModalForm>
    );
}

export default CreateUserModal;
