// src/components/admin/posts/EditPostModal.jsx
import React, { useState, useEffect } from "react";
import ModalForm from "../../ui/ModalForm";
import { apiPut } from "../../../utils/api";

function EditPostModal({ isOpen, post, onClose, onSuccess }) {
    const [title, setTitle] = useState("");
    const [content, setContent] = useState("");
    const [status, setStatus] = useState("");

    useEffect(() => {
        if (post) {
            setTitle(post.title || "");
            setContent(post.content || "");
        }
    }, [post]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setStatus("");
        try {
            if (!post) throw new Error("No post selected");
            const res = await apiPut(`/posts/${post.id}`, { title, content });
            if (!res.ok) {
                const data = await res.json().catch(() => ({}));
                throw new Error(data.detail || "Error updating post");
            }
            setStatus(`✅ Post #${post.id} updated`);
            setTitle("");
            setContent("");
            onSuccess();
            onClose();
        } catch (err) {
            setStatus(err.message || "Error updating post");
        }
    };

    if (!isOpen || !post) return null;

    return (
        <ModalForm
            title={`Edit Post #${post.id}`}
            onCancel={onClose}
            onSubmit={handleSubmit}
            status={status}
            submitLabel="Save Changes"
        >
            <div>
                <label className="block text-xs font-medium text-slate-600 mb-1">
                    Title
                </label>
                <input
                    className="w-full border border-slate-300 rounded-lg px-2 py-1.5 focus:ring-2 focus:ring-sky-500 text-sm"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    required
                />
            </div>
            <div>
                <label className="block text-xs font-medium text-slate-600 mb-1">
                    Content
                </label>
                <textarea
                    className="w-full border border-slate-300 rounded-lg px-2 py-1.5 focus:ring-2 focus:ring-sky-500 text-sm resize-y"
                    rows={6}
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                    required
                />
            </div>
        </ModalForm>
    );
}

export default EditPostModal;
