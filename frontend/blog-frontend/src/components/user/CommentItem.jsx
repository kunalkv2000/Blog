// src/components/user/CommentItem.jsx
import React, { useState } from "react";
import DOMPurify from "dompurify";

function CommentItem({ comment, currentUser, onEdit, onDelete }) {
    const [isEditing, setIsEditing] = useState(false);
    const [editingText, setEditingText] = useState(comment.content);

    const handleSave = () => {
        onEdit(comment.id, editingText);
        setIsEditing(false);
    };

    const handleCancel = () => {
        setEditingText(comment.content);
        setIsEditing(false);
    };

    return (
        <li className="border border-slate-200 rounded-lg px-3 py-2 bg-slate-50">
            {isEditing ? (
                <div>
                    <textarea
                        className="w-full border rounded-lg px-3 py-2 text-sm"
                        rows={3}
                        value={editingText}
                        onChange={(e) => setEditingText(e.target.value)}
                    />
                    <div className="mt-2 flex gap-2 justify-end">
                        <button
                            className="text-xs px-2 py-1 bg-slate-200 rounded"
                            onClick={handleCancel}
                        >
                            Cancel
                        </button>
                        <button
                            className="text-xs px-2 py-1 bg-sky-600 text-white rounded"
                            onClick={handleSave}
                        >
                            Save
                        </button>
                    </div>
                </div>
            ) : (
                <>
                    <div className="flex items-start gap-3">
                        <img
                            src={
                                comment.author_avatar ||
                                "https://ui-avatars.com/api/?name=User"
                            }
                            alt={comment.author_name || "User"}
                            className="w-8 h-8 rounded-full"
                        />
                        <div className="flex-1">
                            <div className="flex items-center justify-between">
                                <div className="text-sm font-medium text-slate-700">
                                    {comment.author_name || "Unknown"}
                                </div>
                                <div className="text-[11px] text-slate-500">
                                    {comment.created_at
                                        ? new Date(comment.created_at).toLocaleString()
                                        : ""}
                                </div>
                            </div>
                            <p
                                className="text-slate-800 mt-1"
                                dangerouslySetInnerHTML={{
                                    __html: DOMPurify.sanitize(comment.content)
                                }}
                            />
                        </div>
                    </div>

                    {/* actions: edit/delete for comment owner or admin */}
                    {currentUser &&
                        (currentUser.id === comment.user_id ||
                            currentUser.role === "admin") && (
                            <div className="mt-2 flex gap-2">
                                <button
                                    className="text-xs text-sky-600 hover:underline"
                                    onClick={() => setIsEditing(true)}
                                >
                                    Edit
                                </button>
                                <button
                                    className="text-xs text-red-600 hover:underline"
                                    onClick={() => onDelete(comment.id)}
                                >
                                    Delete
                                </button>
                            </div>
                        )}
                </>
            )}
        </li>
    );
}

export default CommentItem;
