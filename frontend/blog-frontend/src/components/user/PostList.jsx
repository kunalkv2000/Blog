// src/components/user/PostList.jsx
import React from "react";

function PostList({ posts, activePost, onSelectPost }) {
    return (
        <section className="lg:w-1/3 bg-white rounded-xl shadow-sm border border-slate-200 p-4">
            <h2 className="text-sm font-semibold mb-3">Posts</h2>
            {posts.length === 0 ? (
                <p className="text-xs text-slate-500">No posts yet.</p>
            ) : (
                <ul className="space-y-2 text-sm">
                    {posts.map((post) => (
                        <li key={post.id}>
                            <button
                                onClick={() => onSelectPost(post)}
                                className={`w-full text-left px-3 py-2 rounded-lg border ${activePost && activePost.id === post.id
                                        ? "bg-sky-50 border-sky-200 text-sky-800"
                                        : "bg-white border-slate-200 hover:bg-slate-50"
                                    }`}
                            >
                                <div className="font-semibold truncate">{post.title}</div>
                                <div className="text-xs text-slate-500">
                                    #{post.id} •{" "}
                                    {post.created_at
                                        ? new Date(post.created_at).toLocaleDateString()
                                        : ""}
                                </div>
                            </button>
                        </li>
                    ))}
                </ul>
            )}
        </section>
    );
}

export default PostList;
