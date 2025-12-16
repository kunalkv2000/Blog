import React from "react";
import CommentList from "./CommentList";
import CommentForm from "./CommentForm";

function BlogPostModal({ post, comments, currentUser, onClose, onAddComment, onEditComment, onDeleteComment }) {
    if (!post) return null;

    return (
        <div
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4"
            onClick={onClose}
        >
            <div
                className="bg-white rounded-2xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col"
                onClick={(e) => e.stopPropagation()}
            >
                {/* Modal Header */}
                <div className="bg-indigo-600 p-6 relative">
                    <button
                        onClick={onClose}
                        className="absolute top-4 right-4 text-white/80 hover:text-white bg-white/10 hover:bg-white/20 rounded-full p-2 transition-all"
                    >
                        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                    <h1 className="text-2xl md:text-3xl font-bold text-white pr-12 break-words">
                        {post.title}
                    </h1>
                    <p className="text-white/80 text-sm mt-2">
                        Post #{post.id} • {post.created_at ? new Date(post.created_at).toLocaleDateString() : ""}
                    </p>
                </div>

                {/* Modal Body - Scrollable */}
                <div className="flex-1 overflow-y-auto p-6">
                    {/* Post Content */}
                    <div className="prose prose-slate max-w-none mb-8">
                        <p className="text-slate-800 text-base whitespace-pre-line break-words leading-relaxed">
                            {post.content}
                        </p>
                    </div>

                    {/* Comments Section */}
                    <div className="border-t border-slate-200 pt-6">
                        <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z" />
                            </svg>
                            Comments ({comments.length})
                        </h3>

                        {/* Comment Form */}
                        {currentUser && (
                            <div className="mb-6">
                                <CommentForm
                                    onSubmit={onAddComment}
                                />
                            </div>
                        )}

                        {/* Comments List */}
                        <CommentList
                            comments={comments}
                            currentUser={currentUser}
                            onEdit={onEditComment}
                            onDelete={onDeleteComment}
                        />
                    </div>
                </div>
            </div>
        </div>
    );
}

export default BlogPostModal;
