// src/components/admin/users/EditUserModal.jsx
import React, { useState, useEffect } from "react";
import ModalForm from "../../ui/ModalForm";
import { apiPut } from "../../../utils/api";

function EditUserModal({ isOpen, user, onClose, onSuccess }) {
    const [name, setName] = useState("");
    const [role, setRole] = useState("user");
    const [password, setPassword] = useState("");
    const [status, setStatus] = useState("");

    useEffect(() => {
        if (user) {
            setName(user.name || "");
            setRole(user.role || "user");
            setPassword("");
        }
    }, [user]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setStatus("");
        try {
            if (!user) throw new Error("No user selected");
            const payload = { name, role };
            if (password) payload.password = password;
            const res = await apiPut(`/users/${user.id}`, payload);
            if (!res.ok) {
                const data = await res.json().catch(() => ({}));
                throw new Error(data.detail || "Error updating user");
            }
            setStatus(`✅ User #${user.id} updated`);
            setName("");
            setRole("user");
            setPassword("");
            onSuccess();
            onClose();
        } catch (err) {
            setStatus(err.message || "Error updating user");
        }
    };

    if (!isOpen || !user) return null;

    return (
        <ModalForm
            title={`Edit User #${user.id}`}
            onCancel={onClose}
            onSubmit={handleSubmit}
            status={status}
            submitLabel="Save Changes"
        >
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
                    New Password (optional)
                </label>
                <input
                    type="password"
                    className="w-full border border-slate-300 rounded-lg px-2 py-1.5 focus:ring-2 focus:ring-sky-500 text-sm"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
            </div>
        </ModalForm>
    );
}

export default EditUserModal;
