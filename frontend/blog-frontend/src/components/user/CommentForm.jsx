// src/components/user/CommentForm.jsx
import React, { useState } from "react";

function CommentForm({ onSubmit }) {
    const [commentText, setCommentText] = useState("");

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit(commentText);
        setCommentText("");
    };

    return (
        <form onSubmit={handleSubmit} className="mb-4 space-y-2 text-sm">
            <textarea
                className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-sky-500 resize-y"
                rows={3}
                placeholder="Write a comment..."
                value={commentText}
                onChange={(e) => setCommentText(e.target.value)}
                required
            />
            <div className="flex justify-end">
                <button
                    type="submit"
                    className="bg-sky-600 hover:bg-sky-700 text-white text-xs font-medium px-3 py-2 rounded-lg"
                >
                    Submit Comment
                </button>
            </div>
        </form>
    );
}

export default CommentForm;
