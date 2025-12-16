// src/components/admin/users/UserTable.jsx
import React from "react";
import Button from "../../ui/Button";

function UserTable({ users, onEdit, onDelete, onRefresh }) {
    return (
        <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-sm">
            <div className="flex justify-between items-center mb-3">
                <h2 className="text-sm font-semibold">Users</h2>
                <Button
                    onClick={onRefresh}
                    variant="link"
                    size="sm"
                    className="text-xs"
                >
                    Refresh
                </Button>
            </div>
            <div className="overflow-auto rounded-lg border border-slate-200">
                <table className="min-w-full text-xs">
                    <thead className="bg-slate-50 border-b border-slate-200">
                        <tr>
                            <th className="px-3 py-2 text-left font-semibold">Profile</th>
                            <th className="px-3 py-2 text-left font-semibold">User ID</th>
                            <th className="px-3 py-2 text-left font-semibold">Name</th>
                            <th className="px-3 py-2 text-left font-semibold">Email</th>
                            <th className="px-3 py-2 text-left font-semibold">Role</th>
                            <th className="px-3 py-2 text-left font-semibold">Created</th>
                            <th className="px-3 py-2 text-right font-semibold">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {users.length === 0 ? (
                            <tr>
                                <td
                                    colSpan={6}
                                    className="px-3 py-3 text-center text-slate-500"
                                >
                                    No users found.
                                </td>
                            </tr>
                        ) : (
                            users.map((u, idx) => (
                                <tr
                                    key={u.id}
                                    className={`border-b last:border-b-0 ${idx % 2 === 0 ? "bg-white" : "bg-slate-50"
                                        }`}
                                >
                                    <td className="px-3 py-2 font-mono"><img
                                        src={`https://ui-avatars.com/api/?name=${u.name}&background=random&color=fff`}
                                        alt={u.name || "User"}
                                        className="w-8 h-8 rounded-full"
                                    /></td>
                                    <td className="px-3 py-2 font-mono">#{u.id}</td>
                                    <td className="px-3 py-2">{u.name}</td>
                                    <td className="px-3 py-2">{u.email}</td>
                                    <td className="px-3 py-2">{u.role}</td>
                                    <td className="px-3 py-2 text-slate-500">
                                        {u.created_at
                                            ? new Date(u.created_at).toLocaleString()
                                            : ""}
                                    </td>
                                    <td className="px-3 py-2 text-right">
                                        <div className="inline-flex gap-2">
                                            <Button
                                                onClick={() => onEdit(u)}
                                                variant="warning"
                                                size="sm"
                                            >
                                                Edit
                                            </Button>
                                            <Button
                                                variant="delete"
                                                size="sm"
                                                onClick={() => onDelete(u.id)}
                                            >
                                                Delete
                                            </Button>
                                        </div>
                                    </td>
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
}

export default UserTable;
