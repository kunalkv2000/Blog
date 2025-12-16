import React, { useEffect, useState } from "react";
import { apiDelete } from "../../utils/api";
import "../../index.css";
import Button from "../ui/Button";
import PostTable from "./posts/PostTable";
import CreatePostModal from "./posts/CreatePostModal";
import EditPostModal from "./posts/EditPostModal";

function AdminPostsPanel() {
  const API_BASE = import.meta.env.VITE_API_BASE;
  const [posts, setPosts] = useState([]);
  const [selectedPost, setSelectedPost] = useState(null);
  const [status, setStatus] = useState("");
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);

  async function loadPosts() {
    try {
      const res = await fetch(`${API_BASE}/posts/`);
      if (!res.ok) throw new Error("Failed to load posts");
      const data = await res.json();
      setPosts(data);
    } catch (err) {
      setStatus(err.message || "Error loading posts");
    }
  }

  useEffect(() => {
    loadPosts();
  }, []);

  function handleNewPost() {
    setShowCreateModal(true);
  }

  function handleEditPost(post) {
    setSelectedPost(post);
    setShowEditModal(true);
  }

  async function handleDeletePost(postId) {
    if (!window.confirm(`Delete post #${postId}?`)) return;

    try {
      const res = await apiDelete(`/posts/${postId}`);
      if (!res.ok && res.status !== 204) {
        const data = await res.json().catch(() => ({}));
        throw new Error(data.detail || "Error deleting post");
      }
      setStatus(`🗑️ Post #${postId} deleted`);
      loadPosts();
    } catch (err) {
      setStatus(err.message || "Error deleting post");
    }
  }

  function handleCreateSuccess() {
    loadPosts();
    setStatus("✅ Post created successfully");
  }

  function handleEditSuccess() {
    loadPosts();
    setStatus("✅ Post updated successfully");
  }

  return (
    <div className="p-6 bg-slate-100 max-h-screen">
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between">
        <h1 className="text-2xl font-bold lg:col-span-3 mb-4">Manage Post</h1>
        <Button
          onClick={handleNewPost}
          variant="primary"
          className="lg:col-span-3 mb-4"
        >
          New Post
        </Button>
      </div>

      {status && (
        <div className="mb-4 text-xs text-slate-700 bg-slate-50 border border-slate-200 px-3 py-2 rounded-lg">
          {status}
        </div>
      )}

      <div className="grid grid-cols-1 gap-6">
        <section className="lg:col-span-1" />
        <section className="lg:col-span-2">
          <PostTable
            posts={posts}
            onEdit={handleEditPost}
            onDelete={handleDeletePost}
            onRefresh={loadPosts}
          />
        </section>
      </div>

      <CreatePostModal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        onSuccess={handleCreateSuccess}
      />

      <EditPostModal
        isOpen={showEditModal}
        post={selectedPost}
        onClose={() => {
          setShowEditModal(false);
          setSelectedPost(null);
        }}
        onSuccess={handleEditSuccess}
      />
    </div>
  );
}

export default AdminPostsPanel;
