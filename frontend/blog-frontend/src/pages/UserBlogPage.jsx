import React, { useEffect, useState } from "react";
import { apiGet, apiPost, apiPut, apiDelete } from "../utils/api";
import UserHeader from "../components/user/UserHeader";
import BlogCard from "../components/user/BlogCard";
import BlogPostModal from "../components/user/BlogPostModal";

function UserBlogPage({ currentUser, onLogout }) {
  const [posts, setPosts] = useState([]);
  const [selectedPost, setSelectedPost] = useState(null);
  const [comments, setComments] = useState([]);
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(true);

  async function loadPosts() {
    try {
      setLoading(true);
      const res = await apiGet(`/posts/`);
      if (!res.ok) throw new Error("Failed to load posts");
      const data = await res.json();
      setPosts(data);
    } catch (err) {
      setStatus(err.message || "Error loading posts");
    } finally {
      setLoading(false);
    }
  }

  async function loadComments(postId) {
    try {
      const res = await apiGet(`/comments/post/${postId}`);
      if (!res.ok) throw new Error("Failed to load comments");
      const data = await res.json();
      setComments(data);
    } catch (err) {
      setStatus(err.message || "Error loading comments");
    }
  }

  useEffect(() => {
    loadPosts();
  }, []);

  function openPost(post) {
    setSelectedPost(post);
    loadComments(post.id);
  }

  function closeModal() {
    setSelectedPost(null);
    setComments([]);
  }

  async function handleAddComment(commentText) {
    if (!selectedPost) return;

    try {
      const res = await apiPost(`/comments/`, {
        content: commentText,
        post_id: selectedPost.id,
      });
      if (!res.ok) throw new Error("Failed to submit comment");
      loadComments(selectedPost.id);
      setStatus("Comment added successfully!");
      setTimeout(() => setStatus(""), 3000);
    } catch (err) {
      setStatus(err.message || "Error submitting comment");
    }
  }

  async function handleEditComment(commentId, editingText) {
    try {
      const res = await apiPut(`/comments/${commentId}`, {
        content: editingText,
      });
      if (!res.ok) throw new Error("Failed to update comment");
      loadComments(selectedPost.id);
      setStatus("Comment updated!");
      setTimeout(() => setStatus(""), 3000);
    } catch (err) {
      setStatus(err.message || "Error updating comment");
    }
  }

  async function handleDeleteComment(commentId) {
    if (!window.confirm("Delete this comment?")) return;
    try {
      const res = await apiDelete(`/comments/${commentId}`);
      if (res.status !== 204) throw new Error("Failed to delete comment");
      loadComments(selectedPost.id);
      setStatus("Comment deleted!");
      setTimeout(() => setStatus(""), 3000);
    } catch (err) {
      setStatus(err.message || "Error deleting comment");
    }
  }

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-slate-50 via-white to-slate-100">
      <UserHeader currentUser={currentUser} onLogout={onLogout} />

      {status && (
        <div className="px-6 py-3 bg-sky-50 border-b border-sky-200 text-sm text-sky-800 text-center">
          {status}
        </div>
      )}

      {/* Main content */}
      <main className="flex-1 container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-slate-900 mb-2">
            Explore Blogs
          </h1>
          <p className="text-slate-600">
            Discover insightful articles and engaging content from our community
          </p>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="flex justify-center items-center py-20">
            <div className="animate-spin rounded-full h-12 w-12 border-4 border-sky-500 border-t-transparent"></div>
          </div>
        )}

        {/* Posts Grid */}
        {!loading && posts.length === 0 && (
          <div className="text-center py-20">
            <svg className="w-16 h-16 mx-auto text-slate-300 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z" />
            </svg>
            <h3 className="text-xl font-semibold text-slate-700 mb-2">No posts yet</h3>
            <p className="text-slate-500">Check back later for new content!</p>
          </div>
        )}

        {!loading && posts.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 lg:gap-8">
            {posts.map((post) => (
              <BlogCard
                key={post.id}
                post={post}
                onClick={() => openPost(post)}
              />
            ))}
          </div>
        )}
      </main>

      {/* Blog Post Modal */}
      {selectedPost && (
        <BlogPostModal
          post={selectedPost}
          comments={comments}
          currentUser={currentUser}
          onClose={closeModal}
          onAddComment={handleAddComment}
          onEditComment={handleEditComment}
          onDeleteComment={handleDeleteComment}
        />
      )}
    </div>
  );
}

export default UserBlogPage;
