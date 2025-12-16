// src/components/user/CommentList.jsx
import React from "react";
import CommentItem from "./CommentItem";

function CommentList({ comments, currentUser, onEdit, onDelete }) {
    if (comments.length === 0) {
        return (
            <p className="text-xs text-slate-500">
                No comments yet. Be the first to comment!
            </p>
        );
    }

    return (
        <ul className="space-y-2 text-sm">
            {comments.map((c) => (
                <CommentItem
                    key={c.id}
                    comment={c}
                    currentUser={currentUser}
                    onEdit={onEdit}
                    onDelete={onDelete}
                />
            ))}
        </ul>
    );
}

export default CommentList;
