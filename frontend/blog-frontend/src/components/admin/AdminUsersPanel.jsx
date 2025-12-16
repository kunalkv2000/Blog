// src/components/admin/AdminUsersPanel.jsx
import React, { useEffect, useState } from "react";
import { apiDelete } from "../../utils/api";
import Button from "../ui/Button";
import UserTable from "./users/UserTable";
import CreateUserModal from "./users/CreateUserModal";
import EditUserModal from "./users/EditUserModal";

function AdminUsersPanel() {
  const API_BASE = import.meta.env.VITE_API_BASE;
  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState(null);
  const [status, setStatus] = useState("");
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);

  async function loadUsers() {
    try {
      const res = await fetch(`${API_BASE}/users/`);
      if (!res.ok) throw new Error("Failed to load users");
      const data = await res.json();
      setUsers(data);
    } catch (err) {
      setStatus(err.message || "Error loading users");
    }
  }

  useEffect(() => {
    loadUsers();
  }, []);

  function handleNewUser() {
    setShowCreateModal(true);
  }

  function handleEditUser(user) {
    setSelectedUser(user);
    setShowEditModal(true);
  }

  async function handleDeleteUser(userId) {
    if (!window.confirm(`Delete user #${userId}?`)) return;

    try {
      const res = await apiDelete(`/users/${userId}`);
      if (!res.ok && res.status !== 204) {
        const data = await res.json().catch(() => ({}));
        throw new Error(data.detail || "Error deleting user");
      }
      setStatus(`🗑️ User #${userId} deleted`);
      loadUsers();
    } catch (err) {
      setStatus(err.message || "Error deleting user");
    }
  }

  function handleCreateSuccess() {
    loadUsers();
    setStatus("✅ User created successfully");
  }

  function handleEditSuccess() {
    loadUsers();
    setStatus("✅ User updated successfully");
  }

  return (
    <div className="p-6 bg-slate-100 min-h-screen">
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between mb-6">
        <h1 className="text-2xl font-bold lg:col-span-3 mb-4">Manage Users</h1>
        <Button onClick={handleNewUser} className="lg:col-span-3 mb-4">
          New User
        </Button>
      </div>

      {status && (
        <div className="mb-4 text-xs text-slate-700 bg-slate-50 border border-slate-200 px-3 py-2 rounded-lg">
          {status}
        </div>
      )}

      <div className="grid grid-cols-1 gap-6">
        {/* Left column intentionally empty; create/edit use modals */}
        <section className="lg:col-span-1" />
        {/* Table */}
        <section className="lg:col-span-2">
          <UserTable
            users={users}
            onEdit={handleEditUser}
            onDelete={handleDeleteUser}
            onRefresh={loadUsers}
          />
        </section>
      </div>

      <CreateUserModal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        onSuccess={handleCreateSuccess}
      />

      <EditUserModal
        isOpen={showEditModal}
        user={selectedUser}
        onClose={() => {
          setShowEditModal(false);
          setSelectedUser(null);
        }}
        onSuccess={handleEditSuccess}
      />
    </div>
  );
}

export default AdminUsersPanel;
