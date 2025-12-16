import React from "react";
import DOMPurify from "dompurify";

function PostDetail({ post }) {
    if (!post) {
        return (
            <p className="text-sm text-slate-500">
                Select a post.
            </p>
        );
    }

    return (
        <div className="mb-4">
            <h2 className="text-xl font-semibold mb-1">{post.title}</h2>
            <p className="text-xs text-slate-500 mb-3">
                Post #{post.id} •{" "}
                {post.created_at ? new Date(post.created_at).toLocaleString() : ""}
            </p>
            <p
                className="text-sm text-slate-800 whitespace-pre-line"
                dangerouslySetInnerHTML={{
                    __html: DOMPurify.sanitize(post.content)
                }}
            />
        </div>
    );
}

export default PostDetail;
