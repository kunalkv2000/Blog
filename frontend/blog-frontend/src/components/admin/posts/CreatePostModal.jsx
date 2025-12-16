import React, { useState } from "react";
import ModalForm from "../../ui/ModalForm";
import { apiPost } from "../../../utils/api";

function CreatePostModal({ isOpen, onClose, onSuccess }) {
    const [title, setTitle] = useState("");
    const [content, setContent] = useState("");
    const [status, setStatus] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();
        setStatus("");
        try {
            const res = await apiPost(`/posts/`, { title, content });
            if (!res.ok) {
                const data = await res.json().catch(() => ({}));
                throw new Error(data.detail || "Error creating post");
            }
            setStatus("✅ Post created");
            setTitle("");
            setContent("");
            onSuccess();
            onClose();
        } catch (err) {
            setStatus(err.message || "Error creating post");
        }
    };

    if (!isOpen) return null;

    return (
        <ModalForm
            title="Create Post"
            onCancel={onClose}
            onSubmit={handleSubmit}
            status={status}
            submitLabel="Create Post"
        >
            <div>
                <label htmlFor="post-title" className="block text-xs font-medium text-slate-600 mb-1">
                    Title
                </label>
                <input
                    id="post-title"
                    className="w-full border border-slate-300 rounded-lg px-2 py-1.5 focus:ring-2 focus:ring-sky-500 text-sm"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    required
                />
            </div>
            <div>
                <label htmlFor="post-content" className="block text-xs font-medium text-slate-600 mb-1">
                    Content
                </label>
                <textarea
                    id="post-content"
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

export default CreatePostModal;
